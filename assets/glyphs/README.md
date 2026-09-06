# Wulfpack Forge in-app glyphs

The item masters in `items/` are original Wulfpack Forge artwork created for the desktop application. They are not extracted, traced, or adapted from Valheim or VikingEditor assets.

Each master is a 512×512 transparent grayscale PNG. The application selects a silhouette from the bundled item metadata and applies a restrained material tint at runtime. Unknown or modded prefab IDs receive a neutral generic-material glyph; glyph selection never changes the stored prefab or any save data.

Runtime smoke validation checks that all 23 required files are present, uniquely named, decodable, 512×512, and alpha-capable. Visual legibility remains a human-review responsibility and was checked at the 56 px application size and at the 32 px design target.

The approved generation prompts and the remaining appearance-thumbnail backlog are recorded in `docs/IMAGE_GEN_INDEX.md`. File integrity hashes are recorded in `SHA256SUMS`.
