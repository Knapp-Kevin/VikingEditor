# Architecture

Wulfpack Forge is intentionally small. Its architecture is organized around one principle: make character editing easy at the surface while keeping save handling conservative underneath.

## Runtime shape

```text
Player
  │
  ▼
PySide6 desktop UI
  │
  ├── character discovery
  ├── appearance / inventory / skills / stats editors
  └── save orchestration
        │
        ▼
Valheim character parser / serializer
        │
        ▼
verification + backup + atomic replacement
        │
        ▼
local .fch file
```

Wulfpack Forge does not use a server or remote database for normal operation. Character files are read from the local machine.

## Major components

### `ui/`

Owns the player-facing desktop experience.

- `mainWindow.py` coordinates discovery, loading, editing, and saving.
- `branding.py` resolves Wulfpack Forge product metadata and bundled assets.
- editor tabs own their respective user controls and data mapping.

The UI should not bypass the save-safety layer.

### `subscripts/characterDiscovery.py`

Finds `.fch` files in supported local Valheim directories and Steam userdata locations.

A Steam Cloud entry is discoverable only when a synchronized copy exists on disk. This component does not connect to remote Steam Cloud services.

### `subscripts/fchUtil.py`

Provides low-level Valheim `.fch` parsing and compilation behavior inherited and extended from the VikingEditor codebase.

Normal product flows should use the strict verification layer rather than relying on permissive parser behavior alone.

### `subscripts/playerDataUtil.py`

Decodes and repacks the character's inner player-data payload.

### `subscripts/saveSafety.py`

Owns the write-safety boundary:

1. validate generated candidate;
2. verify checksum and structure;
3. reparse and compare expected root data;
4. create a timestamped backup when replacing an existing destination;
5. atomically replace the destination.

If verification fails, replacement must not occur.

### `data/`

Separates discoverability metadata from write policy.

- `valheim_items.json` is generated, versioned item metadata.
- `items.py` loads catalog data and owns curated safety constraints/resolution behavior.

A catalog refresh must not silently alter write constraints.

### `tools/update_item_catalog.py`

Generates the versioned vanilla item snapshot and guards against unexpected source-version drift or suspiciously incomplete output.

### `tests/`

Provides behavioral evidence for save safety, discovery, catalog handling, UI widgets, branding assets, and related regression boundaries.

## Save lifecycle

### Load

1. Discover or manually select a local `.fch` file.
2. Strictly verify the save envelope/checksum.
3. Parse outer character data.
4. Decode player payload.
5. Populate editor tabs.

A save that cannot be verified is not loaded into the normal editing flow.

### Save

1. Collect changes from editor tabs.
2. Repack player data.
3. Serialize the expected root structure.
4. Compile to a temporary `.fch` candidate in the destination directory.
5. Verify and reparse the candidate.
6. Re-check that Valheim is not running.
7. Back up an existing destination.
8. Atomically replace the destination.

The destination is never the scratch space.

## Packaging

`WulfpackForge.spec` defines the PyInstaller package.

The bundle includes:

- Python application/runtime code;
- `data/valheim_items.json`;
- `assets/wulfpack-forge-banner.jpg`.

The packaged smoke test verifies that critical generated and branding assets can be resolved from the PyInstaller runtime environment.

## Compatibility boundary

Game-version compatibility is explicit state, not an assumption.

A new Valheim version can affect:

- item catalog contents;
- save version fields;
- serialized player structures;
- accepted ranges or semantics;
- in-game acceptance of edited saves.

Major versions therefore require evidence beyond unit tests. See `GOVERNANCE.md` and issue #2.

## Extension rules

New editor capabilities should:

- preserve unrelated data;
- remain human-readable in the normal UI;
- keep raw/modded escape hatches when appropriate;
- add tests at the narrowest stable boundary;
- avoid coupling UI widgets directly to unsafe file replacement logic.

The architecture should remain boring where possible. Boring save code is a feature.