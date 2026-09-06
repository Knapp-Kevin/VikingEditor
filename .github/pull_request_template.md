## What changed

<!-- Describe the user-facing or engineering change. -->

## Why

<!-- What player or maintenance problem does this solve? -->

## Validation

- [ ] `python -m unittest discover -s tests -v`
- [ ] `python -m compileall data subscripts ui tools main.py`
- [ ] Windows packaged-app workflow required for this change and green, or not applicable

Additional evidence:

<!-- Manual checks, screenshots, disposable-save validation, etc. -->

## Save-safety / compatibility impact

- [ ] No save parsing, serialization, constraints, backup/replacement, or compatibility behavior changed
- [ ] This PR does affect one or more of those areas, and the risk/validation is described below

Risk notes:

<!-- Explain affected safety invariants, compatibility assumptions, and recovery behavior. -->

## Documentation

- [ ] README reviewed/updated if player-visible behavior changed
- [ ] CHANGELOG reviewed/updated for user-facing changes
- [ ] SUPPORT / GOVERNANCE reviewed if troubleshooting or policy changed
- [ ] No documentation update is required

## Attribution and product boundary

- [ ] Wulfpack Forge branding and VikingEditor/miskamero attribution remain intact
- [ ] This PR targets `Knapp-Kevin/WulfPackForge`; it is not intended for upstream submission unless explicitly stated

## Checklist

- [ ] Change is focused and does not contain unrelated cleanup
- [ ] Tests cover the behavior being changed
- [ ] Unknown/modded data remains preserved unless intentionally changed by the user
- [ ] Compatibility claims are evidence-backed rather than assumed