"""Glyph and tint resolution for inventory icons.

Glyph ids and tints follow docs/IMAGE_GEN_INDEX.md. Resolution is a pure
function of the catalog row so the renderer can cache by (glyph, tint).
"""
from typing import Optional, Tuple

from data.items import ItemDefinition

GLYPH_MASTER_DIR = "assets/glyphs/items"
DEFAULT_GLYPH = "G20_ingot"
DEFAULT_TINT = "slate"

TINTS = {
    "slate": "#7d7f83",
    "wood": "#8a5a2b",
    "stone": "#7d7f83",
    "bronze": "#b07a2a",
    "iron": "#5c6068",
    "blackmetal": "#2f3238",
    "silver": "#c9d2dc",
    "bone": "#e6dcc3",
    "flame": "#d9531e",
    "eitr": "#4fb3ff",
}

# Ordered: the first token found in the prefab decides the tint.
TINT_TOKENS = (
    ("flametal", "flame"), ("blackmetal", "blackmetal"), ("black_metal", "blackmetal"),
    ("ashlands", "flame"), ("lava", "flame"), ("fire", "flame"),
    ("eitr", "eitr"), ("mistlands", "eitr"), ("dvergr", "eitr"), ("staff", "eitr"),
    ("silver", "silver"), ("frost", "silver"), ("crystal", "silver"),
    ("bone", "bone"), ("antler", "bone"), ("chitin", "bone"), ("carapace", "bone"),
    ("bronze", "bronze"), ("copper", "bronze"), ("tin", "bronze"),
    ("iron", "iron"),
    ("stone", "stone"), ("flint", "stone"), ("obsidian", "stone"),
    ("wood", "wood"), ("yggdrasil", "wood"), ("root", "wood"), ("bow", "wood"),
)

# Prefab-prefix refinements inside a type; checked before the type default.
_PREFIX_GLYPHS = (
    ("sword", "G01_sword"), ("axe", "G02_axe"), ("battleaxe", "G07_battleaxe"),
    ("mace", "G03_mace"), ("club", "G03_mace"), ("sledge", "G09_sledge"),
    ("knife", "G04_knife"), ("spear", "G05_spear"), ("atgeir", "G08_polearm"),
    ("staff", "G10_staff"), ("crossbow", "G12_crossbow"), ("bow", "G11_bow"),
)

GLYPH_BY_TYPE = {
    "OneHandedWeapon": "G01_sword",
    "TwoHandedWeapon": "G06_greatsword",
    "TwoHandedWeaponLeft": "G10_staff",
    "Bow": "G11_bow",
    "Ammo": "G13_arrow",
    "AmmoNonEquipable": "G13_arrow",
    "Shield": "G14_shield",
    "Helmet": "G15_helmet",
    "Chest": "G16_chest",
    "Legs": "G17_legs",
    "Shoulder": "G18_cape",
    "Trinket": "G19_trinket",
    "Utility": "G19_trinket",
    "Material": "G20_ingot",
    "Consumable": "G21_food",
    "Fish": "G21_food",
    "Trophy": "G22_trophy",
    "Torch": "G23_torch",
    "Misc": "G23_torch",
    "Tool": "G02_axe",
}


def tint_for(prefab: str) -> str:
    lowered = prefab.lower()
    for token, tint in TINT_TOKENS:
        if token in lowered:
            return tint
    return DEFAULT_TINT


def _glyph_for_prefix(prefab: str, item_type: Optional[str]) -> Optional[str]:
    lowered = prefab.lower()
    if item_type in {"OneHandedWeapon", "TwoHandedWeapon", "TwoHandedWeaponLeft", "Bow", "Tool"}:
        # Longer prefixes first so "battleaxe" beats "axe" and "crossbow" beats "bow".
        for prefix, glyph in sorted(_PREFIX_GLYPHS, key=lambda pair: -len(pair[0])):
            if lowered.startswith(prefix):
                return glyph
    return None


def glyph_for(item: Optional[ItemDefinition]) -> Tuple[str, str]:
    """``(glyph_id, tint_name)`` for a catalog item; slate ingot for anything unknown."""
    if item is None:
        return DEFAULT_GLYPH, DEFAULT_TINT
    glyph = _glyph_for_prefix(item.prefab, item.item_type) or GLYPH_BY_TYPE.get(item.item_type or "", DEFAULT_GLYPH)
    return glyph, tint_for(item.prefab)
