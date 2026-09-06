"""Curated inventory categories derived from the catalog's ``item_type``.

The grouping is data, not widget logic, so the picker, tests, and any future
surface share one definition.
"""
from typing import Iterable, List, Optional

from data.items import ITEMS, ItemDefinition

GROUPS = (
    "Weapons",
    "Bows and Ammo",
    "Armor",
    "Shields",
    "Tools and Utility",
    "Materials",
    "Food and Mead",
    "Trophies",
    "Misc",
)

GROUP_TYPES = {
    "Weapons": frozenset({"OneHandedWeapon", "TwoHandedWeapon", "TwoHandedWeaponLeft"}),
    "Bows and Ammo": frozenset({"Bow", "Ammo", "AmmoNonEquipable"}),
    "Armor": frozenset({"Helmet", "Chest", "Legs", "Shoulder"}),
    "Shields": frozenset({"Shield"}),
    "Tools and Utility": frozenset({"Tool", "Torch", "Utility", "Trinket"}),
    "Materials": frozenset({"Material"}),
    "Food and Mead": frozenset({"Consumable", "Fish"}),
    "Trophies": frozenset({"Trophy"}),
    "Misc": frozenset({"Misc"}),
}

# Hair and beard rows appear in the JotunnDoc item list but are not inventory items.
EXCLUDED_TYPES = frozenset({"Customization"})

# Progression order used to sort items within a group. Earlier tokens win when
# several appear in one prefab name.
MATERIAL_TIERS = (
    "Wood", "Stone", "Flint", "Leather", "Troll", "Bone", "Bronze", "Copper", "Tin",
    "Iron", "Root", "Silver", "Wolf", "Fenring", "Padded", "Blackmetal", "BlackMetal",
    "Chitin", "Carapace", "Eitr", "Dvergr", "Mistlands", "Ashlands", "Flametal",
    "Fire", "Lava",
)
_TIER_INDEX = {token.lower(): index for index, token in enumerate(MATERIAL_TIERS)}
_TYPE_TO_GROUP = {item_type: group for group, types in GROUP_TYPES.items() for item_type in types}


def group_for(item: Optional[ItemDefinition]) -> Optional[str]:
    """Group name for a catalog item, ``None`` when the item is not pickable."""
    if item is None or item.item_type in EXCLUDED_TYPES:
        return None
    return _TYPE_TO_GROUP.get(item.item_type or "", "Misc")


def tier_rank(prefab: str) -> int:
    lowered = prefab.lower()
    ranks = [index for token, index in _TIER_INDEX.items() if token in lowered]
    return min(ranks) if ranks else len(MATERIAL_TIERS)


def _sorted(items: Iterable[ItemDefinition]) -> List[ItemDefinition]:
    return sorted(items, key=lambda item: (tier_rank(item.prefab), item.display_name.lower(), item.prefab.lower()))


def items_in_group(name: str) -> List[ItemDefinition]:
    return _sorted(item for item in ITEMS if group_for(item) == name)


def pickable_items() -> List[ItemDefinition]:
    """Every selectable catalog item that belongs to a group, sorted by display name."""
    return sorted(
        (item for item in ITEMS if group_for(item) is not None),
        key=lambda item: (item.display_name.lower(), item.prefab.lower()),
    )
