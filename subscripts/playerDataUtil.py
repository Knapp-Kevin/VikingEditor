import struct
import io

class PlayerDataReader:
    def __init__(self, data: bytes):
        self.stream = io.BytesIO(data)

    def read_bytes(self, n: int) -> bytes:
        data = self.stream.read(n)
        if len(data) != n:
            raise EOFError(f"Unexpected end of stream: expected {n} bytes, got {len(data)}")
        return data

    def read_int32(self) -> int:
        return struct.unpack("<i", self.read_bytes(4))[0]

    def read_float(self) -> float:
        return struct.unpack("<f", self.read_bytes(4))[0]

    def read_long(self) -> int:
        return struct.unpack("<q", self.read_bytes(8))[0]

    def read_bool(self) -> bool:
        return self.read_bytes(1)[0] != 0

    def read_7bit_encoded_int(self) -> int:
        value = 0
        shift = 0
        while True:
            byte = self.read_bytes(1)[0]
            value |= (byte & 0x7F) << shift
            if (byte & 0x80) == 0:
                break
            shift += 7
        return value

    def read_string(self) -> str:
        length = self.read_7bit_encoded_int()
        if length == 0:
            return ""
        return self.read_bytes(length).decode("utf-8", errors="ignore")


class PlayerDataWriter:
    def __init__(self):
        self.stream = io.BytesIO()

    def get_bytes(self) -> bytes:
        return self.stream.getvalue()

    def write_int32(self, val: int):
        self.stream.write(struct.pack("<i", val))

    def write_float(self, val: float):
        self.stream.write(struct.pack("<f", val))

    def write_long(self, val: int):
        self.stream.write(struct.pack("<q", val))

    def write_bool(self, val: bool):
        self.stream.write(b"\x01" if val else b"\x00")

    def write_7bit_encoded_int(self, value: int):
        while value >= 0x80:
            self.stream.write(bytes([(value & 0x7F) | 0x80]))
            value >>= 7
        self.stream.write(bytes([value]))

    def write_string(self, val: str):
        encoded = val.encode("utf-8")
        self.write_7bit_encoded_int(len(encoded))
        self.stream.write(encoded)


def unpack_player_data_hex(hex_string: str) -> dict:
    """Parses nested Player.Save payload from hex string into a Python dictionary."""
    if not hex_string:
        return {}
        
    raw_bytes = bytes.fromhex(hex_string)
    pkg = PlayerDataReader(raw_bytes)
    out = {}

    # Player core stats
    out["version"] = pkg.read_int32()  # Normally 29
    out["max_health"] = pkg.read_float()
    out["health"] = pkg.read_float()
    out["max_stamina"] = pkg.read_float()
    out["time_since_death"] = pkg.read_float()
    out["guardian_power"] = pkg.read_string()
    out["guardian_power_cooldown"] = pkg.read_float()

    # Inventory
    out["inventory_version"] = pkg.read_int32()  # Normally 106
    item_count = pkg.read_int32()
    out["inventory"] = []

    for _ in range(item_count):
        item = {
            "prefab": pkg.read_string(),
            "stack": pkg.read_int32(),
            "durability": pkg.read_float(),
            "grid_x": pkg.read_int32(),
            "grid_y": pkg.read_int32(),
            "equipped": pkg.read_bool(),
            "quality": pkg.read_int32(),
            "variant": pkg.read_int32(),
            "crafter_id": pkg.read_long(),
            "crafter_name": pkg.read_string()
        }
        
        custom_count = pkg.read_int32()
        item["custom_data"] = {}
        for _ in range(custom_count):
            key = pkg.read_string()
            val = pkg.read_string()
            item["custom_data"][key] = val
            
        item["world_level"] = pkg.read_int32()
        item["picked_up"] = pkg.read_bool()
        out["inventory"].append(item)

    # Recipes
    count = pkg.read_int32()
    out["known_recipes"] = [pkg.read_string() for _ in range(count)]

    # Known Stations
    count = pkg.read_int32()
    out["known_stations"] = {pkg.read_string(): pkg.read_int32() for _ in range(count)}

    # Materials
    count = pkg.read_int32()
    out["known_material"] = [pkg.read_string() for _ in range(count)]

    # Tutorials
    count = pkg.read_int32()
    out["shown_tutorials"] = [pkg.read_string() for _ in range(count)]

    # Uniques
    count = pkg.read_int32()
    out["uniques"] = [pkg.read_string() for _ in range(count)]

    # Trophies
    count = pkg.read_int32()
    out["trophies"] = [pkg.read_string() for _ in range(count)]

    # Known Biomes
    count = pkg.read_int32()
    out["known_biomes"] = [pkg.read_int32() for _ in range(count)]

    # Known Texts
    count = pkg.read_int32()
    out["known_texts"] = {pkg.read_string(): pkg.read_string() for _ in range(count)}

    # Player Appearance
    out["beard"] = pkg.read_string()
    out["hair"] = pkg.read_string()
    out["skin_color"] = [pkg.read_float(), pkg.read_float(), pkg.read_float()]
    out["hair_color"] = [pkg.read_float(), pkg.read_float(), pkg.read_float()]
    out["model_index"] = pkg.read_int32()

    # Foods
    count = pkg.read_int32()
    out["foods"] = [{"name": pkg.read_string(), "time": pkg.read_float()} for _ in range(count)]

    # Skills
    out["skill_version"] = pkg.read_int32()  # Normally 2
    count = pkg.read_int32()
    out["skills"] = []
    for _ in range(count):
        out["skills"].append({
            "id": pkg.read_int32(),
            "level": pkg.read_float(),
            "xp": pkg.read_float()
        })

    # Custom data
    count = pkg.read_int32()
    out["custom_data"] = {pkg.read_string(): pkg.read_string() for _ in range(count)}

    # Stamina, Max Eitr, Eitr
    out["stamina"] = pkg.read_float()
    out["max_eitr"] = pkg.read_float()
    out["eitr"] = pkg.read_float()

    return out


def pack_player_data_hex(data: dict) -> str:
    """Serializes Player data payload dictionary back into a binary hex string."""
    pkg = PlayerDataWriter()

    # Core Stats
    pkg.write_int32(data.get("version", 29))
    pkg.write_float(data.get("max_health", 25.0))
    pkg.write_float(data.get("health", 25.0))
    pkg.write_float(data.get("max_stamina", 50.0))
    pkg.write_float(data.get("time_since_death", 0.0))
    pkg.write_string(data.get("guardian_power", ""))
    pkg.write_float(data.get("guardian_power_cooldown", 0.0))

    # Inventory
    pkg.write_int32(data.get("inventory_version", 106))
    inventory = data.get("inventory", [])
    pkg.write_int32(len(inventory))
    for item in inventory:
        pkg.write_string(item.get("prefab", ""))
        pkg.write_int32(item.get("stack", 1))
        pkg.write_float(item.get("durability", 100.0))
        pkg.write_int32(item.get("grid_x", 0))
        pkg.write_int32(item.get("grid_y", 0))
        pkg.write_bool(item.get("equipped", False))
        pkg.write_int32(item.get("quality", 1))
        pkg.write_int32(item.get("variant", 0))
        pkg.write_long(item.get("crafter_id", 0))
        pkg.write_string(item.get("crafter_name", ""))
        
        custom_data = item.get("custom_data", {})
        pkg.write_int32(len(custom_data))
        for k, v in custom_data.items():
            pkg.write_string(k)
            pkg.write_string(v)
            
        pkg.write_int32(item.get("world_level", 0))
        pkg.write_bool(item.get("picked_up", False))

    # Recipes
    recipes = data.get("known_recipes", [])
    pkg.write_int32(len(recipes))
    for recipe in recipes:
        pkg.write_string(recipe)

    # Stations
    stations = data.get("known_stations", {})
    pkg.write_int32(len(stations))
    for k, v in stations.items():
        pkg.write_string(k)
        pkg.write_int32(v)

    # Materials
    materials = data.get("known_material", [])
    pkg.write_int32(len(materials))
    for material in materials:
        pkg.write_string(material)

    # Tutorials
    tutorials = data.get("shown_tutorials", [])
    pkg.write_int32(len(tutorials))
    for tutorial in tutorials:
        pkg.write_string(tutorial)

    # Uniques
    uniques = data.get("uniques", [])
    pkg.write_int32(len(uniques))
    for unique in uniques:
        pkg.write_string(unique)

    # Trophies
    trophies = data.get("trophies", [])
    pkg.write_int32(len(trophies))
    for trophy in trophies:
        pkg.write_string(trophy)

    # Biomes
    biomes = data.get("known_biomes", [])
    pkg.write_int32(len(biomes))
    for biome in biomes:
        pkg.write_int32(biome)

    # Known Texts
    texts = data.get("known_texts", {})
    pkg.write_int32(len(texts))
    for k, v in texts.items():
        pkg.write_string(k)
        pkg.write_string(v)

    # Appearance
    # pkg.write_string(data.get("beard", ""))
    # pkg.write_string(data.get("hair", ""))
    # for x in data.get("skin_color", [1.0, 1.0, 1.0]):
    #     pkg.write_float(x)
    # for x in data.get("hair_color", [1.0, 1.0, 1.0]):
    #     pkg.write_float(x)
    # pkg.write_int32(data.get("model_index", 0))
    appearance_start = pkg.stream.tell()

    pkg.write_string(data.get("beard", ""))
    pkg.write_string(data.get("hair", ""))

    for x in data.get("skin_color", [1.0, 1.0, 1.0]):
        pkg.write_float(x)

    for x in data.get("hair_color", [1.0, 1.0, 1.0]):
        pkg.write_float(x)

    pkg.write_int32(data.get("model_index", 0))

    appearance_end = pkg.stream.tell()

    appearance_bytes = pkg.get_bytes()[appearance_start:appearance_end]

    # print("=== APPEARANCE BINARY ===")
    # print("Beard:", repr(data.get("beard")))
    # print("Hair:", repr(data.get("hair")))
    # print("Bytes:", appearance_bytes.hex(" "))

    # Foods
    foods = data.get("foods", [])
    pkg.write_int32(len(foods))
    for food in foods:
        pkg.write_string(food.get("name", ""))
        pkg.write_float(food.get("time", 0.0))

    # Skills
    pkg.write_int32(data.get("skill_version", 2))
    skills = data.get("skills", [])
    pkg.write_int32(len(skills))
    for skill in skills:
        pkg.write_int32(skill.get("id", 0))
        pkg.write_float(skill.get("level", 1.0))
        pkg.write_float(skill.get("xp", 0.0))

    # Custom Data
    c_data = data.get("custom_data", {})
    pkg.write_int32(len(c_data))
    for k, v in c_data.items():
        pkg.write_string(k)
        pkg.write_string(v)

    # Final Stats
    pkg.write_float(data.get("stamina", 50.0))
    pkg.write_float(data.get("max_eitr", 0.0))
    pkg.write_float(data.get("eitr", 0.0))

    return pkg.get_bytes().hex()
