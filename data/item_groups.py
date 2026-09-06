"""Curated inventory navigation: category, then subtype, then material.

Grouping is data, not widget logic, so the picker, tests, and any future
surface share one definition. Roles and slots come from ``data.equipment``.
"""
from typing import Iterable, List, Optional, Tuple

from data.equipment import role_for
from data.glyphs import glyph_for
from data.items import ITEMS, ItemDefinition

GROUPS = (
    "Weapons",
    "Bows and Ammo",
    "Shields",
    "Helmets",
    "Chest Armor",
    "Leg Armor",
    "Capes",
    "Clothing and Hats",
    "Accessories",
    "Tools",
    "Materials",
    "Food and Mead",
    "Trophies",
    "Misc",
    "Creature Gear",
)

# Hair and beard rows appear in the JotunnDoc item list but are not inventory items.
EXCLUDED_TYPES = frozenset({"Customization"})

_TYPE_GROUP = {
    "OneHandedWeapon": "Weapons", "TwoHandedWeapon": "Weapons", "TwoHandedWeaponLeft": "Weapons",
    "Bow": "Bows and Ammo", "Ammo": "Bows and Ammo", "AmmoNonEquipable": "Bows and Ammo",
    "Shield": "Shields", "Helmet": "Helmets", "Chest": "Chest Armor", "Legs": "Leg Armor",
    "Shoulder": "Capes", "Utility": "Accessories", "Trinket": "Accessories",
    "Tool": "Tools", "Torch": "Tools", "Material": "Materials",
    "Consumable": "Food and Mead", "Fish": "Food and Mead", "Trophy": "Trophies", "Misc": "Misc",
}

# Progression order used to sort items within a group and to name material branches.
MATERIAL_TIERS = (
    "Wood", "Stone", "Flint", "Leather", "Troll", "Bone", "Bronze", "Copper", "Tin",
    "Iron", "Root", "Silver", "Wolf", "Fenring", "Padded", "Blackmetal", "BlackMetal",
    "Chitin", "Carapace", "Eitr", "Dvergr", "Mistlands", "Ashlands", "Flametal",
    "Fire", "Lava",
)
_TIER_INDEX = {token.lower(): index for index, token in enumerate(MATERIAL_TIERS)}
_MATERIAL_LABEL = {"BlackMetal": "Blackmetal"}

_SUBTYPE_LABEL = {
    "G01_sword": "Swords", "G02_axe": "Axes", "G03_mace": "Maces", "G04_knife": "Knives",
    "G05_spear": "Spears", "G06_greatsword": "Greatswords", "G07_battleaxe": "Battleaxes",
    "G08_polearm": "Polearms", "G09_sledge": "Sledges", "G10_staff": "Staves",
    "G11_bow": "Bows", "G12_crossbow": "Crossbows", "G13_arrow": "Arrows",
}
_SUBTYPE_ORDER = tuple(_SUBTYPE_LABEL.values()) + ("Bolts",)
_BRANCHED_GROUPS = frozenset({"Weapons", "Bows and Ammo"})


def group_for(item: Optional[ItemDefinition]) -> Optional[str]:
    """Group name for a catalog item, ``None`` when the item is not pickable."""
    if item is None or item.item_type in EXCLUDED_TYPES:
        return None
    role = role_for(item)
    if role == "creature":
        return "Creature Gear"
    if role == "clothing":
        return "Clothing and Hats"
    return _TYPE_GROUP.get(item.item_type or "", "Misc")


def tier_rank(prefab: str) -> int:
    lowered = prefab.lower()
    ranks = [index for token, index in _TIER_INDEX.items() if token in lowered]
    return min(ranks) if ranks else len(MATERIAL_TIERS)


def material_for(item: ItemDefinition) -> Optional[str]:
    rank = tier_rank(item.prefab)
    if rank >= len(MATERIAL_TIERS):
        return None
    token = MATERIAL_TIERS[rank]
    return _MATERIAL_LABEL.get(token, token)


def subgroup_for(item: ItemDefinition) -> Optional[str]:
    if group_for(item) not in _BRANCHED_GROUPS:
        return None
    if item.prefab.lower().startswith("bolt"):
        return "Bolts"
    return _SUBTYPE_LABEL.get(glyph_for(item)[0])


def _sorted(items: Iterable[ItemDefinition]) -> List[ItemDefinition]:
    return sorted(items, key=lambda item: (tier_rank(item.prefab), item.display_name.lower(), item.prefab.lower()))


def items_in_group(name: str) -> List[ItemDefinition]:
    return _sorted(item for item in ITEMS if group_for(item) == name)


def items_under(group: str, subgroup: Optional[str] = None, material: Optional[str] = None) -> List[ItemDefinition]:
    """Items beneath a navigation node; any level may be omitted to widen the selection."""
    return [
        item for item in items_in_group(group)
        if (subgroup is None or subgroup_for(item) == subgroup)
        and (material is None or material_for(item) == material)
    ]


def navigation_tree() -> List[Tuple[str, List[Tuple[str, List[str]]]]]:
    """``[(group, [(subgroup, [material, ...]), ...]), ...]`` in display order."""
    tree = []
    for group in GROUPS:
        branches: List[Tuple[str, List[str]]] = []
        if group in _BRANCHED_GROUPS:
            items = items_in_group(group)
            present = {subgroup_for(item) for item in items} - {None}
            for subgroup in [s for s in _SUBTYPE_ORDER if s in present]:
                materials = []
                for item in items_under(group, subgroup):
                    label = material_for(item)
                    if label and label not in materials:
                        materials.append(label)
                branches.append((subgroup, materials if len(materials) > 1 else []))
        tree.append((group, branches))
    return tree


def pickable_items() -> List[ItemDefinition]:
    """Every selectable catalog item that belongs to a group, sorted by display name."""
    return sorted(
        (item for item in ITEMS if group_for(item) is not None),
        key=lambda item: (item.display_name.lower(), item.prefab.lower()),
    )
