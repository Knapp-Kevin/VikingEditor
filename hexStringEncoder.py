import json
import struct
import io
import sys

stream = None

# write functions
def write_int(value):
    stream.write(struct.pack("<i", value))

def write_float(value):
    stream.write(struct.pack("<f", value))

def write_long(value):
    stream.write(struct.pack("<q", value))

def write_bool(value):
    stream.write(b"\x01" if value else b"\x00")

def write_string(value):
    data = value.encode("utf-8")
    length = len(data)

    while length >= 0x80:
        stream.write(bytes([(length & 0x7F) | 0x80]))
        length >>= 7
    stream.write(bytes([length]))
    stream.write(data)

# pack player data into binary format
def pack_player(data):
    global stream
    stream = io.BytesIO()

    # Player header
    write_int(29)
    write_float(data["max_health"])
    write_float(data["health"])
    write_float(data["max_stamina"])
    write_float(data["time_since_death"])
    write_string(data["guardian_power"])
    write_float(data["guardian_power_cooldown"])

    # Inventory
    write_int(106)
    write_int(len(data["inventory"]))
    for item in data["inventory"]:
        write_string(item["prefab"])
        write_int(item["stack"])
        write_float(item["durability"])
        write_int(item["grid_x"])
        write_int(item["grid_y"])
        write_bool(item["equipped"])
        write_int(item["quality"])
        write_int(item["variant"])
        write_long(item["crafter_id"])
        write_string(item["crafter_name"])
        write_int(len(item["custom_data"]))
        for k,v in item["custom_data"].items():
            write_string(k)
            write_string(v)
        write_int(item["world_level"])
        write_bool(item["picked_up"])

    # Recipes
    write_int(len(data["known_recipes"]))
    for x in data["known_recipes"]:
        write_string(x)

    # Stations
    write_int(len(data["known_stations"]))
    for k,v in data["known_stations"].items():
        write_string(k)
        write_int(v)

    # Materials
    write_int(len(data["known_material"]))
    for x in data["known_material"]:
        write_string(x)

    # Tutorials
    write_int(len(data["shown_tutorials"]))
    for x in data["shown_tutorials"]:
        write_string(x)

    # Uniques
    write_int(len(data["uniques"]))
    for x in data["uniques"]:
        write_string(x)

    # Trophies
    write_int(len(data["trophies"]))
    for x in data["trophies"]:
        write_string(x)

    # Biomes
    write_int(len(data["known_biomes"]))
    for x in data["known_biomes"]:
        write_int(x)

    # Known texts
    write_int(len(data["known_texts"]))
    for k,v in data["known_texts"].items():
        write_string(k)
        write_string(v)

    # Appearance
    write_string(data["beard"])
    write_string(data["hair"])

    for x in data["skin_color"]:
        write_float(x)
    for x in data["hair_color"]:
        write_float(x)
    write_int(data["model_index"])

    # Foods
    write_int(len(data["foods"]))
    for food in data["foods"]:
        write_string(food["name"])
        write_float(food["time"])

    # Skills
    write_int(2)
    write_int(len(data["skills"]))
    for skill in data["skills"]:
        write_int(skill["id"])
        write_float(skill["level"])
        write_float(skill["xp"])

    # Custom data
    write_int(len(data["custom_data"]))
    for k,v in data["custom_data"].items():
        write_string(k)
        write_string(v)

    # Final stats
    write_float(data["stamina"])
    write_float(data["max_eitr"])
    write_float(data["eitr"])
    return stream.getvalue()

if len(sys.argv) != 2:
    print("Usage:")
    print(" python hexStringEncoder.py playerdata.json")
    sys.exit()

with open(sys.argv[1], "r", encoding="utf-8") as f:
    data = json.load(f)

binary = pack_player(data)

with open("player_data_hex.txt", "w") as f:
    f.write(binary.hex())

print("Packed", len(binary), "bytes")
