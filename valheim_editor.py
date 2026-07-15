import sys
import os
import json
import struct
import io
import hashlib

# binary read and write utils

class BinaryReader:
    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)

    def read_bytes(self, n: int) -> bytes:
        return self.stream.read(n)

    def read_int32(self) -> int:
        return struct.unpack("<i", self.stream.read(4))[0]

    def read_float(self) -> float:
        return struct.unpack("<f", self.stream.read(4))[0]

    def read_bool(self) -> bool:
        return struct.unpack("?", self.stream.read(1))[0]

    def read_long(self) -> int:
        return struct.unpack("<q", self.stream.read(8))[0]

    def read_vector3(self) -> list:
        return list(struct.unpack("<fff", self.stream.read(12)))

    def read_7bit_encoded_int(self) -> int:
        value = 0
        shift = 0
        while True:
            byte = self.stream.read(1)[0]
            value |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:
                break
            shift += 7
        return value

    def read_string(self) -> str:
        length = self.read_7bit_encoded_int()
        return self.stream.read(length).decode("utf-8")

    def read_byte_array(self) -> bytes:
        length = self.read_int32()
        return self.stream.read(length)


class BinaryWriter:
    def __init__(self):
        self.stream = io.BytesIO()

    def get_bytes(self) -> bytes:
        return self.stream.getvalue()

    def write_bytes(self, data: bytes):
        self.stream.write(data)

    def write_int32(self, val: int):
        self.stream.write(struct.pack("<i", val))

    def write_float(self, val: float):
        self.stream.write(struct.pack("<f", val))

    def write_bool(self, val: bool):
        self.stream.write(struct.pack("?", val))

    def write_long(self, val: int):
        self.stream.write(struct.pack("<q", val))

    def write_vector3(self, val: list):
        self.stream.write(struct.pack("<fff", *val))

    def write_7bit_encoded_int(self, value: int):
        while value >= 0x80:
            self.stream.write(bytes([(value & 0x7F) | 0x80]))
            value >>= 7
        self.stream.write(bytes([value]))

    def write_string(self, val: str):
        encoded = val.encode("utf-8")
        self.write_7bit_encoded_int(len(encoded))
        self.stream.write(encoded)

    def write_byte_array(self, data: bytes):
        self.write_int32(len(data))
        self.stream.write(data)

# unpack .fch to .json

def decompile_fch(fch_path: str, json_path: str):
    print(f"Reading binary save: {fch_path}")
    with open(fch_path, "rb") as f:
        file_bytes = f.read()

    file_reader = BinaryReader(file_bytes)
    zpackage_len = file_reader.read_int32()
    zpackage_bytes = file_reader.read_bytes(zpackage_len)
    
    # checksum validation
    hash_len = file_reader.read_int32()
    stored_hash = file_reader.read_bytes(hash_len)

    # verify integrity, klinoff certified
    calculated_hash = hashlib.sha512(zpackage_bytes).digest()
    if calculated_hash != stored_hash:
        print("Warning: File SHA-512 checksum mismatch. Save may be corrupted, but we'll try to parse it anyway.")

    pkg = BinaryReader(zpackage_bytes)
    save_data = {}

    version = pkg.read_int32()
    save_data["version"] = version
    
    if version != 43:
        print(f"Warning: This script is configured for Version 43. Attempting to parse Version {version} anyway...")

    # 1. read stats and skills
    stat_count = pkg.read_int32()
    save_data["stats"] = [pkg.read_float() for _ in range(stat_count)]

    # 2. first spawn boolean
    save_data["first_spawn"] = pkg.read_bool()

    # 3. world data
    world_count = pkg.read_int32()
    worlds = []
    for _ in range(world_count):
        world = {}
        world["world_id"] = pkg.read_long()
        world["have_custom_spawn"] = pkg.read_bool()
        world["spawn_point"] = pkg.read_vector3()
        world["have_logout_point"] = pkg.read_bool()
        world["logout_point"] = pkg.read_vector3()

        if version >= 30:
            world["have_death_point"] = pkg.read_bool()
            world["death_point"] = pkg.read_vector3()

        world["home_point"] = pkg.read_vector3()
        has_map_data = pkg.read_bool()
        world["map_data_hex"] = pkg.read_byte_array().hex() if has_map_data else None
        worlds.append(world)
    save_data["worlds"] = worlds

    # 4. char info
    save_data["character_name"] = pkg.read_string()
    save_data["player_id"] = pkg.read_long()
    save_data["start_seed"] = pkg.read_string()

    # 5. metadata (v38+)
    save_data["used_cheats"] = pkg.read_bool()
    save_data["date_created_unix"] = pkg.read_long()

    # known worlds
    known_worlds_count = pkg.read_int32()
    save_data["known_worlds"] = {pkg.read_string(): pkg.read_float() for _ in range(known_worlds_count)}

    # known world keys
    known_keys_count = pkg.read_int32()
    save_data["known_world_keys"] = {pkg.read_string(): pkg.read_float() for _ in range(known_keys_count)}

    # known console commands
    known_cmds_count = pkg.read_int32()
    save_data["known_commands"] = {pkg.read_string(): pkg.read_float() for _ in range(known_cmds_count)}

    # v42+ stats dictionaries
    if version >= 42:
        enemy_stats_count = pkg.read_int32()
        save_data["enemy_stats"] = {pkg.read_string(): pkg.read_float() for _ in range(enemy_stats_count)}

        pickup_stats_count = pkg.read_int32()
        save_data["item_pickup_stats"] = {pkg.read_string(): pkg.read_float() for _ in range(pickup_stats_count)}

        craft_stats_count = pkg.read_int32()
        save_data["item_craft_stats"] = {pkg.read_string(): pkg.read_float() for _ in range(craft_stats_count)}

    # 6. player data
    has_player_data = pkg.read_bool()
    save_data["player_data_hex"] = pkg.read_byte_array().hex() if has_player_data else None

    # output to json
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(save_data, f, indent=4)
    print(f"Successfully unpacked save! JSON created at: {json_path}")

# .json to .fch

def compile_fch(json_path: str, fch_path: str):
    print(f"Reading JSON file: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        save_data = json.load(f)

    pkg = BinaryWriter()
    version = save_data["version"]
    pkg.write_int32(version)

    # 1. stats and skills
    pkg.write_int32(len(save_data["stats"]))
    for stat in save_data["stats"]:
        pkg.write_float(stat)

    # 2. first spawn boolean
    pkg.write_bool(save_data["first_spawn"])

    # 3. world data
    pkg.write_int32(len(save_data["worlds"]))
    for world in save_data["worlds"]:
        pkg.write_long(world["world_id"])
        pkg.write_bool(world["have_custom_spawn"])
        pkg.write_vector3(world["spawn_point"])
        pkg.write_bool(world["have_logout_point"])
        pkg.write_vector3(world["logout_point"])

        if version >= 30:
            pkg.write_bool(world["have_death_point"])
            pkg.write_vector3(world["death_point"])

        pkg.write_vector3(world["home_point"])
        has_map_data = world["map_data_hex"] is not None
        pkg.write_bool(has_map_data)
        if has_map_data:
            pkg.write_byte_array(bytes.fromhex(world["map_data_hex"]))

    # 4. char info
    pkg.write_string(save_data["character_name"])
    pkg.write_long(save_data["player_id"])
    pkg.write_string(save_data["start_seed"])

    # 5. metadata (v38+)
    pkg.write_bool(save_data["used_cheats"])
    pkg.write_long(save_data["date_created_unix"])

    # known worlds
    pkg.write_int32(len(save_data["known_worlds"]))
    for k, v in save_data["known_worlds"].items():
        pkg.write_string(k)
        pkg.write_float(v)

    # known world keys
    pkg.write_int32(len(save_data["known_world_keys"]))
    for k, v in save_data["known_world_keys"].items():
        pkg.write_string(k)
        pkg.write_float(v)

    # known console cmds
    pkg.write_int32(len(save_data["known_commands"]))
    for k, v in save_data["known_commands"].items():
        pkg.write_string(k)
        pkg.write_float(v)

    # v42+ stats dictionaries
    if version >= 42:
        pkg.write_int32(len(save_data["enemy_stats"]))
        for k, v in save_data["enemy_stats"].items():
            pkg.write_string(k)
            pkg.write_float(v)

        pkg.write_int32(len(save_data["item_pickup_stats"]))
        for k, v in save_data["item_pickup_stats"].items():
            pkg.write_string(k)
            pkg.write_float(v)

        pkg.write_int32(len(save_data["item_craft_stats"]))
        for k, v in save_data["item_craft_stats"].items():
            pkg.write_string(k)
            pkg.write_float(v)

    # 6. player data
    has_player_data = save_data["player_data_hex"] is not None
    pkg.write_bool(has_player_data)
    if has_player_data:
        pkg.write_byte_array(bytes.fromhex(save_data["player_data_hex"]))

    # write to .fch with checksum
    zpackage_bytes = pkg.get_bytes()
    calculated_hash = hashlib.sha512(zpackage_bytes).digest()

    file_writer = BinaryWriter()
    file_writer.write_int32(len(zpackage_bytes))
    file_writer.write_bytes(zpackage_bytes)
    file_writer.write_int32(len(calculated_hash))
    file_writer.write_bytes(calculated_hash)

    with open(fch_path, "wb") as f:
        f.write(file_writer.get_bytes())
    print(f"Successfully compiled and hashed! File created at: {fch_path}")

# interface for cli usage

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Valheim Save File Utility v43")
        print("Usage:")
        print("  Decompile: python valheim_editor.py unpack <character.fch> <output.json>")
        print("  Compile:   python valheim_editor.py pack <input.json> <output.fch>")
        sys.exit(1)

    mode = sys.argv[1].lower()
    source_file = sys.argv[2]
    target_file = sys.argv[3]

    if mode == "unpack":
        decompile_fch(source_file, target_file)
    elif mode == "pack":
        compile_fch(source_file, target_file)
    else:
        print(f"Error: Unknown mode '{mode}'. Use 'unpack' or 'pack'.")
