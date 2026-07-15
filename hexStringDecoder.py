import json
import struct
import io
import sys

stream = None

# read functions

def read_int():
    data = stream.read(4)
    if len(data) != 4:
        raise EOFError("Unexpected end while reading int")
    return struct.unpack("<i", data)[0]


def read_float():
    data = stream.read(4)
    if len(data) != 4:
        raise EOFError("Unexpected end while reading float")
    return struct.unpack("<f", data)[0]


def read_long():
    data = stream.read(8)
    if len(data) != 8:
        raise EOFError("Unexpected end while reading long")
    return struct.unpack("<q", data)[0]


def read_bool():
    data = stream.read(1)
    if len(data) != 1:
        raise EOFError("Unexpected end while reading bool")
    return data[0] != 0


def read_string():
    length = 0
    shift = 0
    while True:
        b = stream.read(1)
        if len(b) == 0:
            raise EOFError("Unexpected end while reading string length")

        b = b[0]
        length |= (b & 0x7F) << shift
        if not (b & 0x80):
            break
        shift += 7
    data = stream.read(length)

    if len(data) != length:
        raise EOFError("Unexpected end while reading string")
    return data.decode("utf-8", errors="ignore")

# unpack

def unpack_mode(filename):
    global stream

    with open(filename, "r", encoding="utf-8") as f:
        save = json.load(f)

    stream = io.BytesIO(
        bytes.fromhex(save["player_data_hex"])
    )
    out = {}

    # player data headers
    out["version"] = read_int()
    out["max_health"] = read_float()
    out["health"] = read_float()
    out["max_stamina"] = read_float()
    out["time_since_death"] = read_float()
    out["guardian_power"] = read_string()
    out["guardian_power_cooldown"] = read_float()

    # inventory
    out["inventory_version"] = read_int()
    item_count = read_int()
    out["inventory"] = []

    for i in range(item_count):
        item = {}
        item["prefab"] = read_string()
        item["stack"] = read_int()
        item["durability"] = read_float()
        item["grid_x"] = read_int()
        item["grid_y"] = read_int()
        item["equipped"] = read_bool()
        item["quality"] = read_int()
        item["variant"] = read_int()
        item["crafter_id"] = read_long()
        item["crafter_name"] = read_string()
        custom_count = read_int()
        item["custom_data"] = {}
        for _ in range(custom_count):
            key = read_string()
            value = read_string()
            item["custom_data"][key] = value
        item["world_level"] = read_int()
        item["picked_up"] = read_bool()
        out["inventory"].append(item)

    # known recipes
    count = read_int()
    out["known_recipes"] = []
    for _ in range(count):
        out["known_recipes"].append(
            read_string()
        )

    # stations
    count = read_int()
    out["known_stations"] = {}
    for _ in range(count):
        key = read_string()
        value = read_int()
        out["known_stations"][key] = value

    # materials
    count = read_int()
    out["known_material"] = []
    for _ in range(count):
        out["known_material"].append(
            read_string()
        )

    # tutorials
    count = read_int()
    out["shown_tutorials"] = []
    for _ in range(count):
        out["shown_tutorials"].append(
            read_string()
        )

    # uniques
    count = read_int()
    out["uniques"] = []

    for _ in range(count):
        out["uniques"].append(
            read_string()
        )

    # trophies
    count = read_int()
    out["trophies"] = []
    for _ in range(count):
        out["trophies"].append(
            read_string()
        )

    # known biomes
    count = read_int()
    out["known_biomes"] = []
    for _ in range(count):
        out["known_biomes"].append(
            read_int()
        )

    # known texts

    count = read_int()
    out["known_texts"] = {}
    for _ in range(count):
        key = read_string()
        value = read_string()
        out["known_texts"][key] = value


    # player appearance
    out["beard"] = read_string()
    out["hair"] = read_string()
    out["skin_color"] = [
        read_float(),
        read_float(),
        read_float()
    ]
    out["hair_color"] = [
        read_float(),
        read_float(),
        read_float()
    ]
    out["model_index"] = read_int()

    # foods
    count = read_int()
    out["foods"] = []
    for _ in range(count):
        out["foods"].append({
            "name": read_string(),
            "time": read_float()
        })

    # skills

    out["skill_version"] = read_int()
    count = read_int()
    out["skills"] = []
    for _ in range(count):
        out["skills"].append({
            "id": read_int(),
            "level": read_float(),
            "xp": read_float()
        })

    # custom data
    count = read_int()
    out["custom_data"] = {}
    for _ in range(count):
        key = read_string()
        value = read_string()
        out["custom_data"][key] = value

    # stats
    out["stamina"] = read_float()
    out["max_eitr"] = read_float()
    out["eitr"] = read_float()

    # write to json
    with open(
        "playerdata.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            out,
            f,
            indent=4,
            ensure_ascii=False
        )

    print("Saved playerdata.json")

if len(sys.argv) != 3:

    print(
        "Usage:\n"
        " python valheim_nested_editor.py unpack save.json"
    )
    sys.exit(1)

mode = sys.argv[1]
filename = sys.argv[2]

if mode == "unpack":
    unpack_mode(filename)

else:
    print("Only unpack implemented currently")
