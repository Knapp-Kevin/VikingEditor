# Governance

Wulfpack Forge is maintained as a safety-first community character editor for Valheim. This document defines how project decisions are made, how compatibility claims are earned, and what must be true before a change can ship.

## Maintainer authority

The repository owner and maintainer, Frostwulf / Knapp-Kevin, is the final decision maker for product direction, releases, compatibility declarations, branding, and merge policy. Contributions are welcome, but no contribution is entitled to merge by virtue of implementation effort alone.

## Project principles

1. **Preserve player data.** A safer write path is preferred over convenience when the two conflict.
2. **Never claim compatibility without evidence.** Game-version support is validated against real saves and the packaged application before release.
3. **Preserve unknown data.** Modded, future-version, and otherwise unrecognized values should be retained whenever practical instead of normalized away.
4. **Player-first UX.** Normal users should not need Python, Git, command-line tools, or save-format knowledge to use the application.
5. **Explicit provenance.** Wulfpack Forge remains clearly attributed to VikingEditor by miskamero and distributed under GPLv3.
6. **Unofficial status.** Nothing in project branding or documentation may imply endorsement by Iron Gate Studio or Coffee Stain Publishing.

## Change classes

### Routine changes

Documentation corrections, small UI refinements, tests, and low-risk maintenance may merge after relevant automated checks pass.

### Save-affecting changes

Any change that can alter serialized `.fch` output must include behavioral tests and must preserve the candidate-first, verify-first, backup-first, atomic-replacement safety model.

### Compatibility changes

Any change that declares support for a new Valheim version must satisfy the compatibility gate below.

### Release/distribution changes

Changes to PyInstaller packaging, dependencies, executable startup, bundled assets, or release automation require a successful Windows packaged-application build and smoke test.

## Compatibility gate

A Valheim version may be described as supported only after all applicable checks pass:

- item catalog version/source reviewed and deliberately advanced where needed
- automated source tests green
- packaged Windows executable built successfully
- packaged executable smoke test green
- real character `.fch` loads successfully
- no-op round trip succeeds
- at least one representative appearance edit succeeds
- inventory edits are validated when item/schema changes are relevant
- backup and atomic replacement behavior remain intact
- edited save is accepted by Valheim and intended changes survive in game

If evidence is incomplete, documentation must say so. Planned or expected compatibility is not supported compatibility.

## Pull requests

Pull requests should be narrowly scoped, explain user-visible behavior, identify save-safety implications, include tests where behavior changes, and update documentation when commands, installation, compatibility, or user workflow changes.

Merge preference is squash merge unless preserving commit history materially improves traceability.

## Issues and roadmap

Issue #2 is the durable product roadmap. Larger feature work should be represented there or in a focused issue linked from it. Completed work should be reconciled back into the roadmap so the issue remains a useful source of truth rather than a museum of unchecked boxes.

## Security and vulnerability handling

Security-sensitive reports should follow `SECURITY.md`. Public issues are appropriate for ordinary bugs, but vulnerabilities that could cause data loss, arbitrary code execution, unsafe file writes, or dependency compromise should not be disclosed publicly before maintainers have had a reasonable opportunity to assess them.

## Documentation standard

README, support, contribution, security, compatibility, and release documentation are treated as product surfaces. User-facing claims must match current code, tests, and release state. Documentation updates are part of implementation when behavior or workflow changes.

## Licensing and attribution

Wulfpack Forge is a modified and expanded derivative of VikingEditor by miskamero and is distributed under GNU GPLv3. Existing license and notice obligations must be preserved in source and binary distributions. The Wulfpack Forge name and derivative branding distinguish this project from the original VikingEditor distribution.
