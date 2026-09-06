<p align="center">
  <img src="assets/wulfpack-forge-banner.jpg" alt="Wulfpack Forge banner" width="1200">
</p>

<h1 align="center">Wulfpack Forge</h1>
<p align="center"><strong>Character Editor for Valheim</strong><br>by Frostwulf</p>
<p align="center"><em>Based on <a href="https://github.com/miskamero/VikingEditor">VikingEditor</a> by miskamero</em></p>

<p align="center">
  <a href="https://github.com/Knapp-Kevin/WulfPackForge/actions/workflows/tests.yml"><img alt="Tests" src="https://github.com/Knapp-Kevin/WulfPackForge/actions/workflows/tests.yml/badge.svg"></a>
  <a href="https://github.com/Knapp-Kevin/WulfPackForge/actions/workflows/package-windows.yml"><img alt="Windows build" src="https://github.com/Knapp-Kevin/WulfPackForge/actions/workflows/package-windows.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: GPLv3" src="https://img.shields.io/badge/license-GPLv3-blue.svg"></a>
</p>

Wulfpack Forge is a player-first desktop editor for Valheim character saves. It is designed for the person who wants to change a beard, hair color, inventory item, skill, or stat without learning Python, searching obscure save folders, or gambling a character file on a direct overwrite.

The normal path is deliberately simple: download the Windows build, open a character that exists locally, make changes, and click **Save Changes**. Underneath that simple workflow, Wulfpack Forge verifies save structure and checksums, creates a protected workspace snapshot and working copy, detects outside changes to the active character, blocks writes while Valheim is running, backs up the active save, and only replaces it after the edited candidate passes validation.

> **Unofficial community software.** Wulfpack Forge is not affiliated with, authorized by, or endorsed by Iron Gate Studio or Coffee Stain Publishing.

## Quick start

### Windows players

1. Open the repository's [Releases](https://github.com/Knapp-Kevin/WulfPackForge/releases) page.
2. Download `WulfpackForge-windows-x64.zip` or `WulfpackForge.exe` from the latest published release.
3. Extract the ZIP if needed.
4. Close Valheim.
5. Launch `WulfpackForge.exe`.
6. Select a discovered character or browse to a `.fch` file.
7. Check the compact character status, make your edits, and click **Save Changes**.
8. Wulfpack Forge verifies the working copy, confirms the active source has not changed, backs up the current active save, and applies the edit.

**No Python, Git, `pip`, or command prompt is required for the packaged Windows build.**

If a packaged release has not been published yet, the source-install path remains available for developers and advanced users under [Running from source](#running-from-source).

## What Wulfpack Forge can edit

| Area | Capabilities |
|---|---|
| Appearance | Skin color, hair color, beard color, hair style, beard style, and supported model settings |
| Inventory | Searchable vanilla item catalog, raw prefab support, stacks, durability, quality, variants, equipped state |
| Skills | Supported Valheim skill levels |
| Stats | Supported health, stamina, progression, and related character values |
| Character details | Supported character-level fields such as name |

Known vanilla items use human-readable names while retaining their prefab IDs. Unknown, modded, or newer-version items are preserved rather than rejected simply because the bundled catalog does not recognize them.

## Character discovery and Steam Cloud

Wulfpack Forge reads **character files that exist on the local computer**.

It searches the normal Valheim local-save directories and Steam userdata locations for `.fch` files that have been synchronized to disk. A character that exists only remotely in Steam Cloud cannot be opened until Steam has downloaded or synchronized a local copy.

If no character appears:

1. Make sure Steam is online and synchronization is complete.
2. Launch Valheim and confirm the character is visible there.
3. Exit Valheim so the save is no longer in use.
4. Return to Wulfpack Forge and click **Refresh**.
5. Use **Browse for Another Save** if you already have the `.fch` file in a custom location.

Wulfpack Forge does **not** connect to a remote Steam Cloud API or download saves directly from Valve.

## Managed character workspace

Opening a verified character creates a Wulfpack Forge workspace outside Valheim's own save directories. On Windows the default root is `%LOCALAPPDATA%\WulfpackForge`.

For each active character, Wulfpack Forge keeps:

```text
WulfpackForge/
└── characters/
    └── active/
        └── <character-id>/
            ├── source/      # immutable snapshots captured when the character is opened
            ├── working/     # current verified Wulfpack Forge working copy
            ├── backups/     # previous active saves preserved before replacement
            └── metadata.json
```

The workspace is deliberately separate from Valheim and Steam directories. Wulfpack Forge does not create organizational folders inside the game's save tree or ask Steam Cloud to synchronize its internal working files.

The source snapshot gives the editing session an immutable baseline. The working copy gives Wulfpack Forge a durable verified representation of the intended edit before the active game file is touched. Immediately before replacement, Wulfpack Forge compares the active character against the hash recorded when it was opened. If Steam, Valheim, another editor, or another process changed that file, saving is blocked and the player is asked to reload rather than overwriting the newer state.

## Character status

The main window exposes a compact status surface instead of hiding safety state in tooltips and dialogs.

Current states are intentionally specific:

- **Verified** means checksum and structure verification passed and the character save version is in Wulfpack Forge's current write-validated set.
- **Compatibility unverified** means the file verifies structurally, but its save version has not been validated for writing. It may be inspected, but **Save Changes** is disabled.
- **Needs attention** means verification failed or the active source changed outside Wulfpack Forge after it was opened.

The status also shows the save version, source, modification time, bundled Valheim catalog version, and the most recent backup when available.

## Save safety

Character editing should not require optimism as a recovery plan. Wulfpack Forge uses a preservation-first write path:

- **Immutable opened snapshot.** A verified copy of the source is preserved in the managed workspace when editing begins.
- **Verified working copy.** The edited candidate is verified and stored in the Wulfpack Forge workspace before the active save is replaced.
- **External-change detection.** The active source hash is checked before replacement so newer Steam, Valheim, or external edits are not silently overwritten.
- **Valheim process protection.** Writes are blocked while Valheim is running, with a second check immediately before replacement.
- **Candidate-first compilation.** Edited data is compiled to a temporary `.fch` candidate rather than written over the destination.
- **Strict SHA-512 verification.** The generated save envelope and checksum are validated.
- **Round-trip verification.** The candidate is reparsed and compared with the expected serialized data.
- **Automatic timestamped backup.** The current active save is copied into the character's Wulfpack Forge workspace before replacement.
- **Atomic replacement.** The active destination changes only after verification succeeds.
- **Failure-safe behavior.** If verification or source-consistency checking fails, the existing active destination is left untouched.

Backups are still worth keeping for characters you care about, especially around major game updates or heavily modded saves. The point is that the editor should add protection, not outsource it to the player's memory.

## Valheim compatibility

The bundled item catalog is currently generated from **Valheim 0.221.12** data and contains more than 900 player-selectable vanilla items.

Valheim 1.0 is scheduled for **September 9, 2026**. Wulfpack Forge will not claim post-1.0 compatibility merely because the application launches. The release gate tracked in [issue #2](https://github.com/Knapp-Kevin/WulfPackForge/issues/2) requires a deliberate catalog refresh plus real 1.0 character-save validation, including load, no-op round trip, appearance editing, inventory editing, backup behavior, atomic replacement, and in-game acceptance.

The current parser/serializer is explicitly validated for character-save version **43**. A structurally valid save using a different character-save version is shown as **Compatibility unverified** and remains read-only until that version has its own evidence.

Until the 1.0 gate passes, unknown items are preserved conservatively. They may be modded content or legitimate items introduced by a newer Valheim build.

## Item catalog design

The player-facing catalog is generated from JotunnDoc vanilla Valheim item data and committed as `data/valheim_items.json`.

Catalog discovery and save-writing constraints are intentionally separated:

- the generated catalog supplies names, types, asset identifiers, selectability, and source-version metadata;
- the curated constraint layer controls known stack, quality, and variant limits;
- a catalog refresh therefore cannot silently loosen save-writing rules;
- raw prefab entry remains available for modded and unknown content.

For the current pre-1.0 snapshot:

```bash
python tools/update_item_catalog.py --expected-version 0.221.12
```

The generator refuses unexpected source-version drift and suspiciously small catalogs so a game update cannot silently rewrite the application data model.

## Running from source

Source installation is intended for contributors, developers, and advanced users.

### Requirements

- Python 3.9+
- Git

### Clone

```bash
git clone https://github.com/Knapp-Kevin/WulfPackForge.git
cd WulfPackForge
```

### Install

```bash
python -m pip install -r requirements.txt
```

### Run

```bash
python main.py
```

## Building the Windows application

The repository uses PyInstaller to produce a self-contained Windows executable. The packaging workflow:

- installs application dependencies;
- runs the automated test suite;
- builds `WulfpackForge.exe`;
- bundles the versioned item catalog and canonical Wulfpack Forge banner;
- smoke-tests the packaged executable and required assets;
- creates a Windows ZIP package;
- generates SHA-256 checksums;
- uploads the build as a workflow artifact;
- publishes release assets for version tags.

## Development and validation

Automated coverage currently includes:

- save-safety behavior;
- checksum and round-trip verification;
- managed workspace snapshots and working copies;
- external active-source change detection;
- workspace-managed backups;
- local and Steam-synchronized character discovery;
- save-health and compatibility-state derivation;
- item catalog generation and version drift;
- catalog resolution and duplicate-name behavior;
- unknown/modded item preservation;
- offscreen Qt widget behavior;
- Wulfpack Forge branding quality and runtime asset validation;
- Python source compilation;
- packaged Windows executable smoke testing.

The durable product roadmap is [issue #2](https://github.com/Knapp-Kevin/WulfPackForge/issues/2).

### UI screenshots

The README will include screenshots of the **actual Wulfpack Forge application**, not mockups, after the current workspace/status UI stabilizes. Screenshot capture and maintenance are tracked in issue #2 so the images represent the shipping interface rather than an intermediate design.

## Project structure

```text
├── main.py
├── assets/
│   └── wulfpack-forge-banner.jpg
├── data/
│   ├── items.py
│   └── valheim_items.json
├── tools/
│   └── update_item_catalog.py
├── subscripts/
│   ├── characterDiscovery.py
│   ├── fchUtil.py
│   ├── playerDataUtil.py
│   ├── saveHealth.py
│   ├── saveSafety.py
│   └── workspace.py
├── ui/
│   ├── branding.py
│   ├── mainWindow.py
│   ├── saveStatusWidget.py
│   ├── appearanceTab.py
│   ├── inventoryTab.py
│   ├── skillsTab.py
│   ├── statsTab.py
│   └── miscTab.py
├── tests/
└── .github/workflows/
```

## Governance and community

Wulfpack Forge is intentionally small, but not undocumented. The repository keeps the rules that matter close to the code:

- [CONTRIBUTING.md](CONTRIBUTING.md) explains development workflow and contribution expectations.
- [GOVERNANCE.md](GOVERNANCE.md) defines maintainer authority, safety invariants, compatibility policy, and release gates.
- [SECURITY.md](SECURITY.md) covers vulnerability and save-integrity reporting.
- [SUPPORT.md](SUPPORT.md) provides player troubleshooting and support boundaries.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) defines community conduct expectations.
- [CHANGELOG.md](CHANGELOG.md) records user-facing changes.

Changes that affect save parsing, save writing, compatibility claims, catalog constraints, or release artifacts require evidence appropriate to the risk. A green interface is not proof that a save editor is safe. Unfortunately, software has made this lesson necessary.

## Project lineage and attribution

**Wulfpack Forge** is a modified and expanded derivative of **VikingEditor** by **miskamero**.

Original project: https://github.com/miskamero/VikingEditor

This distribution preserves the original project's attribution and is distributed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE) and [NOTICE](NOTICE) for the applicable terms and attribution requirements.

The name **Wulfpack Forge** is used for this modified distribution so it is clearly distinguished from the original VikingEditor project.

## Contributing

Issues and pull requests are welcome. Before contributing, read [CONTRIBUTING.md](CONTRIBUTING.md). The core rule is simple: **never make an irreversible save change when a safer path is practical.**

## Disclaimer

Wulfpack Forge modifies Valheim character save data. No save editor can guarantee compatibility with every game update, mod, or future save-format change.

Keep important saves backed up, especially before major Valheim updates or when using modded characters.
