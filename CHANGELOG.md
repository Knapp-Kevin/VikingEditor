# Changelog

All notable user-facing changes to Wulfpack Forge are recorded here.

The project is currently evolving toward its first branded Wulfpack Forge release, so historical work is grouped by implementation milestone rather than retroactively inventing version numbers.

## Unreleased

### Added
- Managed Wulfpack Forge character workspaces outside the Valheim save tree.
- Immutable source snapshots captured when a verified character is opened.
- Durable verified working copies before edits are applied to the active save.
- External active-source change detection to prevent overwriting newer Steam, Valheim, or third-party edits.
- Compact character status surface with `Verified`, `Compatibility unverified`, and `Needs attention` states.
- Save version, source, modification time, catalog version, and recent-backup details in the main UI.
- Workspace-scoped timestamped backups.
- Regression coverage for workspace snapshots, working copies, external-change detection, and workspace backup placement.
- Current application screenshots for the main save-status surface, Appearance tab, and catalog-aware Inventory editor.
- Runtime banner validation that rejects non-image bytes instead of accepting a corrupt file based on size alone.
- Regression coverage for banner decoding and save-status text contrast.

### Changed
- `Save Changes` now applies edits to the active loaded character through the managed workspace safety path rather than asking the player to choose the destination again.
- Backups created during normal editing are kept under the character's Wulfpack Forge workspace instead of cluttering the active Valheim character directory.
- Valid character-save versions outside the current write-validated set are explicitly read-only rather than being treated as silently writable.
- README and support guidance now document the workspace, save-health states, Steam Cloud interaction, and source-change protection.
- The canonical README/application banner was restored from the approved 2048×682 master through a binary-safe local conversion.
- Save-status metadata and guidance now use readable foreground colors on the dark status surface.
- README release media now shows the current application with synthetic, publication-safe character data.

## Branding and governance milestone

Merged in `3f670f3be6a52c4981cbc48f683c4a872de1d635`.

### Added
- Wulfpack Forge product identity and approved wolf banner.
- Branded application header and packaged-brand asset verification.
- Player-facing guidance for Steam Cloud characters that are not yet synchronized locally.
- First-class repository governance, contribution, support, security, architecture, agent, brand, and community documentation.
- Structured issue and pull-request templates.

### Changed
- Repository renamed to `Knapp-Kevin/WulfPackForge`.
- README rewritten around the player journey, current capabilities, compatibility status, safety model, and contributor pathways.
- Application window branding updated from the generic save-editor name to Wulfpack Forge.

## Versioned item catalog milestone

Merged in `4bee65caa90b9cbfeb49f8e753f6a37e63a0233f`.

### Added
- Generated Valheim item catalog pinned to pre-1.0 build `0.221.12`.
- More than 900 player-selectable vanilla catalog entries.
- Catalog source/version metadata and version-drift safeguards.
- Packaged executable verification that the item catalog is bundled correctly.
- Explicit Valheim 1.0 compatibility gate.

### Changed
- Item discovery moved from a small hand-maintained list to generated game-data-backed metadata.
- Duplicate human-readable names require prefab-disambiguated completion labels rather than arbitrary resolution.

## Player-first distribution milestone

Merged in `05e7c8723b343d1490b03d8fd21f65c279202105`.

### Added
- Self-contained Windows `WulfpackForge.exe` build.
- Portable Windows ZIP package and SHA-256 checksums.
- Packaged executable smoke testing in GitHub Actions.

### Changed
- Normal player workflow moved away from Python/Git setup and toward download-and-run distribution.
- Primary UI simplified around character selection, editing, and Save Changes.

## Discovery and item-aware editing milestone

Merged in `f697e9087c07bc6de53653d608c5c008c8b0337c`.

### Added
- Automatic discovery of locally available Valheim character files, including Steam-synchronized copies on disk.
- Strict verification before loading a character.
- Searchable inventory item selection with human-readable names.
- Safe preservation of unknown and modded prefab IDs and unusual existing values.
- Automated tests for discovery, catalog behavior, Qt item editing, and dependencies.

## Save-safety milestone

Merged in `7b86f23e6c7d19fd71df0e29e45aa4404da308f5`.

### Added
- Write blocking while Valheim is running.
- Candidate-first save compilation.
- Strict SHA-512 envelope verification.
- Round-trip reparsing and expected-structure comparison.
- Timestamped backups before replacement.
- Atomic destination replacement only after verification succeeds.
- Regression tests proving failed verification leaves the destination untouched.

## Project lineage

Wulfpack Forge is based on VikingEditor by miskamero and remains distributed under GPLv3. See `NOTICE` and `LICENSE` for attribution and licensing details.
