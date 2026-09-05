import re
from dataclasses import dataclass
from typing import Dict, Iterable, Optional


@dataclass(frozen=True)
class ItemDefinition:
    prefab: str
    display_name: str
    max_stack: Optional[int] = None
    max_quality: Optional[int] = None
    variants: Optional[int] = None

    @property
    def completion_label(self) -> str:
        return f"{self.display_name} — {self.prefab}"


def _humanize_prefab(prefab: str) -> str:
    text = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", prefab)
    return text.replace("_", " ").strip()


def _item(prefab: str, max_stack=None, max_quality=None, variants=None, display_name=None):
    return ItemDefinition(
        prefab=prefab,
        display_name=display_name or _humanize_prefab(prefab),
        max_stack=max_stack,
        max_quality=max_quality,
        variants=variants,
    )


# Conservative baseline catalog. Constraints are included only where the values are
# stable and well-established. Unknown/modded items are intentionally allowed by the UI.
ITEMS = [
    _item("Amber", 20, 1, 1),
    _item("AmberPearl", 50, 1, 1, "Amber Pearl"),
    _item("AncientSeed", 50, 1, 1, "Ancient Seed"),
    _item("BeechSeeds", 100, 1, 1, "Beech Seeds"),
    _item("Barley", 100, 1, 1),
    _item("BarleyFlour", 20, 1, 1, "Barley Flour"),
    _item("BlackMetal", 30, 1, 1, "Black Metal"),
    _item("Bronze", 30, 1, 1),
    _item("Coal", 50, 1, 1),
    _item("Copper", 30, 1, 1),
    _item("FineWood", 50, 1, 1, "Fine Wood"),
    _item("Flametal", 30, 1, 1),
    _item("Iron", 30, 1, 1),
    _item("Obsidian", 50, 1, 1),
    _item("Resin", 50, 1, 1),
    _item("Silver", 30, 1, 1),
    _item("Stone", 50, 1, 1),
    _item("Tin", 30, 1, 1),
    _item("Wood", 50, 1, 1),
    _item("YggdrasilWood", 50, 1, 1, "Yggdrasil Wood"),
    _item("ArrowBronze", 100, 1, 1, "Bronze Arrow"),
    _item("ArrowFire", 100, 1, 1, "Fire Arrow"),
    _item("ArrowFlint", 100, 1, 1, "Flinthead Arrow"),
    _item("ArrowFrost", 100, 1, 1, "Frost Arrow"),
    _item("ArrowIron", 100, 1, 1, "Ironhead Arrow"),
    _item("ArrowNeedle", 100, 1, 1, "Needle Arrow"),
    _item("ArrowObsidian", 100, 1, 1, "Obsidian Arrow"),
    _item("ArrowPoison", 100, 1, 1, "Poison Arrow"),
    _item("ArrowSilver", 100, 1, 1, "Silver Arrow"),
    _item("ArrowWood", 100, 1, 1, "Wood Arrow"),
    _item("AxeStone", 1, 4, 1, "Stone Axe"),
    _item("AxeFlint", 1, 4, 1, "Flint Axe"),
    _item("AxeBronze", 1, 4, 1, "Bronze Axe"),
    _item("AxeIron", 1, 4, 1, "Iron Axe"),
    _item("AxeBlackMetal", 1, 4, 1, "Blackmetal Axe"),
    _item("AtgeirBronze", 1, 4, 1, "Bronze Atgeir"),
    _item("AtgeirIron", 1, 4, 1, "Iron Atgeir"),
    _item("AtgeirBlackmetal", 1, 4, 1, "Blackmetal Atgeir"),
    _item("Battleaxe", 1, 4, 1, "Battleaxe"),
    _item("ArmorBronzeChest", 1, 4, 1, "Bronze Plate Cuirass"),
    _item("ArmorBronzeLegs", 1, 4, 1, "Bronze Plate Leggings"),
    _item("ArmorIronChest", 1, 4, 1, "Iron Scale Mail"),
    _item("ArmorIronLegs", 1, 4, 1, "Iron Greaves"),
    _item("ArmorLeatherChest", 1, 4, 1, "Leather Tunic"),
    _item("ArmorLeatherLegs", 1, 4, 1, "Leather Pants"),
    _item("ArmorPaddedCuirass", 1, 4, 1, "Padded Cuirass"),
    _item("ArmorPaddedGreaves", 1, 4, 1, "Padded Greaves"),
    _item("ArmorRagsChest", 1, 2, 1, "Rag Tunic"),
    _item("ArmorRagsLegs", 1, 2, 1, "Rag Pants"),
    _item("ArmorTrollLeatherChest", 1, 4, 1, "Troll Leather Tunic"),
    _item("ArmorTrollLeatherLegs", 1, 4, 1, "Troll Leather Pants"),
    _item("ArmorWolfChest", 1, 4, 1, "Wolf Armor Chest"),
    _item("ArmorWolfLegs", 1, 4, 1, "Wolf Armor Legs"),
    _item("BeltStrength", 1, 1, 1, "Megingjord"),
    _item("HelmetBronze", 1, 4, 1, "Bronze Helmet"),
    _item("HelmetIron", 1, 4, 1, "Iron Helmet"),
    _item("HelmetPadded", 1, 4, 1, "Padded Helmet"),
    _item("HelmetTrollLeather", 1, 4, 1, "Troll Leather Helmet"),
    _item("HelmetDrake", 1, 4, 1, "Drake Helmet"),
    _item("PickaxeAntler", 1, 1, 1, "Antler Pickaxe"),
    _item("PickaxeBronze", 1, 4, 1, "Bronze Pickaxe"),
    _item("PickaxeIron", 1, 4, 1, "Iron Pickaxe"),
    _item("ShieldWood", 1, 3, 8, "Wood Shield"),
    _item("ShieldBronzeBuckler", 1, 3, 1, "Bronze Buckler"),
    _item("ShieldBanded", 1, 3, 8, "Banded Shield"),
    _item("ShieldBlackmetal", 1, 3, 8, "Black Metal Shield"),
    _item("SwordBronze", 1, 4, 1, "Bronze Sword"),
    _item("SwordIron", 1, 4, 1, "Iron Sword"),
    _item("SwordSilver", 1, 4, 1, "Silver Sword"),
    _item("SwordBlackmetal", 1, 4, 1, "Blackmetal Sword"),
]

ITEMS_BY_PREFAB: Dict[str, ItemDefinition] = {item.prefab.lower(): item for item in ITEMS}
ITEMS_BY_DISPLAY: Dict[str, ItemDefinition] = {item.display_name.lower(): item for item in ITEMS}
ITEMS_BY_COMPLETION: Dict[str, ItemDefinition] = {item.completion_label.lower(): item for item in ITEMS}


def iter_items() -> Iterable[ItemDefinition]:
    return sorted(ITEMS, key=lambda item: (item.display_name.lower(), item.prefab.lower()))


def resolve_item(value: str) -> Optional[ItemDefinition]:
    key = (value or "").strip().lower()
    if not key:
        return None
    return ITEMS_BY_PREFAB.get(key) or ITEMS_BY_DISPLAY.get(key) or ITEMS_BY_COMPLETION.get(key)


def completion_labels():
    return [item.completion_label for item in iter_items()]
