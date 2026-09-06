# Image Generation Index (original glyph set)

## Implementation status

- **Complete:** all 23 inventory glyph masters are approved, bundled under `assets/glyphs/items/`, mapped in `data/glyphs.py`, and rendered with material tinting in the Inventory grid and item editor.
- **Wired, art pending:** 38 hairstyle and 27 beard thumbnails. The Appearance tab and the New Character dialog already show a thumbnail next to any style whose PNG exists under `assets/glyphs/hair/` or `assets/glyphs/beard/` (named by catalog id, e.g. `Hair7.png`, `BeardNone.png`); entries without art stay text-only.

Lists every original image the bundled glyph set needs so the batch can be generated in one pass. Nothing here derives from Iron Gate art; each glyph depicts the concept, in one consistent house style, and is keyed on data the item catalog already carries (`item_type`) plus a material tint inferred from the prefab name. See `docs/BRAND_GUIDE.md` for the product palette this extends.

## Prompt template (paste into the image generator, one glyph per request)

```
Flat vector game inventory icon of a {DEPICTS}, single centred object on a fully transparent background,
one dark charcoal outline, two-tone cel shading, light from the top left, cool slate grey material
(#7d7f83) with no colour tint, no text, no border, no background scene, no drop shadow, square 512x512,
silhouette must stay readable at 32 pixels. Norse-fantasy character editor style, clean and modern,
not photorealistic, not pixel art. Original design, not based on any existing game's art.
```

Generate the 23 item masters in grey; the app applies the material tint at load time. For hair and beard thumbnails use the second template below.

```
Flat vector schematic head-and-shoulders silhouette, front view, neutral face with no features, showing
the hairstyle "{STYLE NAME}" as a solid mid-grey hair mass on a dark charcoal head, transparent background,
one dark outline, no text, square 512x512, readable at 48 pixels. Norse-fantasy character editor style,
original design.
```

## House style (apply to every prompt)

- 64x64 target, authored at 512x512, transparent background, single centred object.
- Flat vector look with one dark outline and two-tone shading; no text, no backgrounds, no borders.
- Consistent light from top-left. Silhouette must read at 32 px.
- Palette: cool slate base; material tint applied only to the object's primary surface.

## Material tints (8)

| tint | hex | applies to prefab tokens |
|---|---|---|
| wood | #8a5a2b | Wood, FineWood, Yggdrasil, Root, Bow (unless metal) |
| stone | #7d7f83 | Stone, Flint, Obsidian |
| bronze | #b07a2a | Bronze, Copper, Tin |
| iron | #5c6068 | Iron, Blackmetal/BlackMetal (darker variant #2f3238) |
| silver | #c9d2dc | Silver, Frost, Crystal |
| bone | #e6dcc3 | Bone, Antler, Chitin, Carapace |
| flame | #d9531e | Flametal, Fire, Ashlands, Lava |
| eitr | #4fb3ff | Eitr, Mistlands, Dvergr, magic staves |

## Item silhouettes (23) with catalog coverage (selectable items, Valheim 0.221.12)

| glyph id | depicts | item_type(s) covered | count |
|---|---|---|---|
| G01 sword | one-handed straight blade | OneHandedWeapon (swords) | part of 90 |
| G02 axe | one-handed axe | OneHandedWeapon (axes), Tool (axes) | part of 90 |
| G03 mace | club or mace | OneHandedWeapon (clubs, maces) | part of 90 |
| G04 knife | dagger | OneHandedWeapon (knives) | part of 90 |
| G05 spear | spear | OneHandedWeapon (spears) | part of 90 |
| G06 greatsword | two-handed sword | TwoHandedWeapon | part of 58 |
| G07 battleaxe | two-handed axe | TwoHandedWeapon | part of 58 |
| G08 polearm | atgeir | TwoHandedWeapon | part of 58 |
| G09 sledge | two-handed hammer | TwoHandedWeapon | part of 58 |
| G10 staff | magic staff | TwoHandedWeapon, TwoHandedWeaponLeft | part of 59 |
| G11 bow | bow | Bow | 22 |
| G12 crossbow | crossbow | Bow (crossbow prefabs) | part of 22 |
| G13 arrow | arrow or bolt | Ammo, AmmoNonEquipable | 31 |
| G14 shield | round shield | Shield | 17 |
| G15 helmet | helmet | Helmet | 42 |
| G16 chest | chest armour | Chest | 52 |
| G17 legs | leg armour | Legs | 21 |
| G18 cape | cloak | Shoulder | 11 |
| G19 trinket | amulet or belt | Trinket, Utility | 25 |
| G20 ingot | material bar or lump | Material | 215 |
| G21 food | bowl or cooked item | Consumable, Fish | 116 |
| G22 trophy | mounted head plaque | Trophy | 60 |
| G23 torch | torch | Torch, Misc | 27 |

Customization (109) is not an inventory surface and needs no glyph. Modded prefabs with no catalog row fall back to G20 with the slate tint.

Batch size: 23 silhouettes x 8 tints = 184 renders, produced by tinting one master per silhouette in code, so the generation task is 23 images.

## Hairstyle thumbnails (38)

One original schematic head-and-shoulders silhouette per entry in `data/hairs.py`, same style, hair mass drawn from the entry's name (Windswept, High Ponytail, Pigtails, Low Ponytail, Short, Long and Loose, Dragonslayer, Parted, Old One-Eye, Side Swept, Long Braid, Matronly, Twin Braids, Speed Demon, Pulled Back Curls, Gathered Braids, Neat Braids, Royal Braids, Painter Curls, Tidy Curls, Twin Buns, Single Bun, Short Curls, Shaved and Braided, Knot, Short Locs, Braids of Strength, Merchant's Braid, Tucked Back, Loose Waves, Gathered Locs, Mullet, Vinland Shave, Castellan, Champion, Chronicler, Sunbringer) plus "No Hair". Hair colour is applied in the app from the save's hair_color.

## Beard thumbnails (27)

One silhouette per catalog beard: Majestic, Twin Braids, Short, Straight, Single Braid, Loose Braid, Split Shave, Thick, Trobadour, Top Braid, Facewarmer, Royal, Triplets, Split Braid, Mini Braid, Stonedweller, Neat, Jarl Braids, Bushy, Spiky, Tidy, Mustache, Crumb Catcher, Waxed, Trimmed, Handlebar (Beard1-Beard26 in that order), plus "No Beard" (BeardNone).

## Output manifest

Approved files move to `assets/glyphs/` as original bundled art. Work in progress stays outside the runtime asset tree:

```
assets/glyphs/items/G01_sword.png ... G23_torch.png   (masters, 512x512, untinted grey)
assets/glyphs/hair/Hair1.png ... Hair37.png, HairNone.png
assets/glyphs/beard/Beard1.png ... Beard26.png, BeardNone.png
```

The app maps prefab -> (glyph, tint) with a small rules table in `data/glyphs.py` and tints at load time. The inventory masters are complete; the hair and beard paths above are picked up automatically once the PNGs exist.
