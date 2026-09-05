# Wulfpack Forge

## Character Editor for Valheim

**by Frostwulf**  
*Based on [VikingEditor](https://github.com/miskamero/VikingEditor) by [miskamero](https://github.com/miskamero)*

Wulfpack Forge is a desktop character editor for **Valheim** designed for players who want to change their character without learning save-file internals, installing developer tools, or manually hunting through folders.

Use it to customize appearance, inventory, skills, stats, and character details through a graphical interface. Wulfpack Forge automatically discovers supported Valheim character saves, verifies them before loading, creates backups before replacement, and refuses to write while Valheim is running.

> **Unofficial community software.** Wulfpack Forge is not affiliated with, authorized by, or endorsed by Iron Gate Studio or Coffee Stain Publishing.

---

## For Players: Download and Run

### Windows

The normal player experience is intended to be simple:

1. Open the repository's **Releases** page.
2. Download `WulfpackForge-windows-x64.zip` or `WulfpackForge.exe` from the latest release.
3. If you downloaded the ZIP, extract it.
4. Launch `WulfpackForge.exe`.
5. Select your Valheim character from the automatically discovered list.
6. Make your changes.
7. Click **Save Changes**.

**You do not need Python, Git, `pip`, or a command prompt to use the packaged Windows build.**

If no packaged release is available yet, see [Running from Source](#running-from-source) below. That path is intended for developers, contributors, and advanced users.

---

## Valheim Version Compatibility

Wulfpack Forge treats game-version compatibility as part of save safety, not as a footnote.

The bundled item catalog is currently generated from **Valheim 0.221.12** data and contains more than 900 player-selectable vanilla items. The catalog records the Valheim version it was generated from and the item editor displays that version when resolving items.

**Valheim 1.0 is scheduled for September 9, 2026.** The 1.0 release includes the Deep North and additional game content, so the item catalog will need to be regenerated after compatible 1.0 game data becomes available. Iron Gate also tested save-system changes ahead of 1.0. Their published details focus primarily on world saves, but Wulfpack Forge will still revalidate real 1.0 character `.fch` loading, editing, round-trip verification, backups, and replacement before declaring a post-1.0 build compatible.

Until that validation is complete, an item not found in the bundled catalog is treated conservatively: Wulfpack Forge preserves the raw prefab and values rather than assuming the item is invalid. It may be a modded item or a legitimate item from a newer Valheim version.

---

## What You Can Edit

### Appearance

Wulfpack Forge opens directly into the appearance-focused experience so common changes are easy to reach.

- Skin color
- Hair color
- Beard color
- Hair style
- Beard style
- Character model / appearance options supported by the save format

### Inventory

- View inventory visually by slot
- Search the bundled vanilla item catalog by human-readable name or prefab
- Use a versioned catalog generated from Valheim game data rather than a small hand-maintained list
- Edit item stack count, durability, quality, variant, and equipped state
- Automatically apply curated known stack, quality, and variant limits
- Preserve unknown, modded, or newer-version prefab IDs instead of rejecting them
- Preserve unusual existing values rather than silently destroying them

Catalog discovery data and save-writing constraints are intentionally separated. Updating the generated item list cannot silently loosen or change stack, quality, or variant limits.

### Skills

View and adjust supported Valheim skill levels through normal UI controls.

### Stats

Edit supported character health, stamina, progression, and related values.

### Character Details

Safely update supported character-level information such as the character name.

---

## Finding Your Character

In most cases, you should not have to find a `.fch` file yourself.

Wulfpack Forge automatically searches supported Valheim character locations, including local saves and supported Steam-synced locations. Discovered characters are shown with useful metadata such as source, modified time, save version when available, and validation state.

If your character lives somewhere unusual, **Browse for .fch** remains available as a manual fallback.

---

## Save Safety

Editing a game save should not require optimism as a recovery strategy. Wulfpack Forge adds several safeguards around writes:

- **Valheim process protection:** saving is blocked while Valheim is running, including a second check immediately before the write.
- **Candidate-first compilation:** edited data is compiled to a temporary candidate instead of overwriting the destination directly.
- **Strict SHA-512 verification:** the generated `.fch` envelope and checksum are validated before replacement.
- **Round-trip verification:** the generated save is reparsed and compared with the expected serialized data.
- **Automatic timestamped backup:** an existing destination save is copied before replacement.
- **Atomic replacement:** the destination is replaced only after the new save has passed verification.
- **Failure-safe behavior:** if verification fails, the destination save is left untouched.

Backups are still worth keeping for anything you care about, but Wulfpack Forge no longer depends on the user remembering to manually make one before every edit.

---

## Typical Workflow

1. Close Valheim.
2. Launch Wulfpack Forge.
3. Choose a discovered character and click **Open Selected**.
4. Edit the character using the relevant tabs.
5. Click **Save Changes**.
6. Wulfpack Forge verifies the new save and creates a backup of the existing destination before replacement.
7. Launch Valheim and confirm the changes.

That is the intended normal-user path. No copying save files around by hand should be necessary for standard installations.

---

## Running from Source

This section is for developers, contributors, or users who specifically want to run the Python source instead of the packaged desktop build.

### Requirements

- Python 3.9+
- Git

### Clone this fork

```bash
git clone https://github.com/Knapp-Kevin/VikingEditor.git
cd VikingEditor
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

### Run

```bash
python main.py
```

---

## Refreshing the Valheim Item Catalog

The player-facing catalog is generated from JotunnDoc's vanilla Valheim item data and committed as `data/valheim_items.json`.

For the currently supported pre-1.0 snapshot:

```bash
python tools/update_item_catalog.py --expected-version 0.221.12
```

The generator records the source Valheim version and refuses to publish a suspiciously small catalog. If the upstream source reports a different game version than expected, generation fails so a game update cannot silently replace the catalog without review.

When Valheim 1.0 data becomes available, update the expected version deliberately, regenerate the catalog, inspect the diff for new/removed items, and run the full character-save compatibility suite before publishing a 1.0-compatible Wulfpack Forge release.

---

## Building the Windows Desktop App

The repository includes a PyInstaller-based Windows packaging workflow. The packaged application is built as a self-contained executable so end users do not need a Python runtime.

The GitHub Actions packaging workflow:

- installs application dependencies
- runs the test suite
- builds `WulfpackForge.exe`
- bundles the versioned Valheim item catalog
- smoke-tests the packaged executable and catalog
- creates a Windows ZIP package
- generates a SHA-256 checksum file
- uploads the build as a workflow artifact
- publishes packaged files to GitHub Releases for version tags

---

## Development and Validation

The fork includes automated validation for the functionality added beyond the original VikingEditor project, including:

- save-safety behavior
- checksum and round-trip verification
- automatic character discovery
- versioned item catalog resolution
- unknown/modded/newer-version item preservation
- offscreen Qt widget behavior
- Python source compilation
- packaged Windows executable and bundled-catalog smoke testing

The broader local roadmap is tracked in [issue #2](https://github.com/Knapp-Kevin/VikingEditor/issues/2). The completed player-installation tranche is recorded in [issue #4](https://github.com/Knapp-Kevin/VikingEditor/issues/4).

---

## Project Structure

```text
├── main.py                       # Application entry point
├── data/
│   ├── items.py                  # Catalog loader + curated safety constraints
│   └── valheim_items.json       # Generated, versioned vanilla item catalog
├── tools/
│   └── update_item_catalog.py    # Version-aware catalog generator
├── subscripts/
│   ├── characterDiscovery.py     # Local and Steam character discovery
│   ├── fchUtil.py                # Valheim .fch parsing/compilation
│   ├── playerDataUtil.py         # Inner character data decoding/packing
│   └── saveSafety.py             # Strict verification, backups, safe replacement
├── ui/
│   ├── mainWindow.py             # Main application window and workflow
│   ├── appearanceTab.py          # Appearance editor
│   ├── inventoryTab.py           # Inventory editor
│   ├── skillsTab.py              # Skill editor
│   ├── statsTab.py               # Stats editor
│   └── miscTab.py                # Character-level settings
├── tests/                        # Regression and behavior tests
└── .github/workflows/            # Test, catalog, and packaging automation
```

---

## Project Lineage and Attribution

**Wulfpack Forge** is a modified and expanded derivative of **VikingEditor** by **miskamero**.

Original project: https://github.com/miskamero/VikingEditor

This fork preserves the original project's attribution and is distributed under the **GNU General Public License v3.0 (GPLv3)**. See [LICENSE](LICENSE) and [NOTICE](NOTICE) for the applicable terms and attribution requirements.

The name **Wulfpack Forge** is used for this modified distribution so it is clearly distinguished from the original VikingEditor project.

---

## Contributing

Issues and pull requests are welcome in this fork. Contributions should preserve the project's core safety principle: **never make an irreversible save change when a safer path is practical.**

When adding editor functionality, prefer human-readable controls while retaining safe escape hatches for modded or unknown game data.

---

## Disclaimer

Wulfpack Forge modifies Valheim character save data. Although the fork performs automatic backup and verification steps, no save editor can guarantee compatibility with every game update, mod, or future save-format change.

Keep important saves backed up, especially before major game updates or when working with modded characters.
