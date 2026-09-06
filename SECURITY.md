# Security and Save Integrity

Wulfpack Forge edits local Valheim character saves. Security for this project includes traditional application vulnerabilities and failures that could corrupt, overwrite, or unexpectedly expose player data.

## Supported code

Security fixes are prioritized for the latest maintained branch and current published release. Older builds may no longer receive fixes after a newer release supersedes them.

## Reporting a vulnerability

Please do not publish exploit details, sensitive local paths, tokens, credentials, or private data in a public issue.

Use GitHub's private vulnerability reporting / Security Advisory flow when it is available for this repository. If that option is unavailable, contact the repository owner privately through the contact information on the maintainer's GitHub profile before disclosing sensitive details publicly.

For non-sensitive save-corruption bugs, a normal GitHub issue is appropriate. Remove personal information and attach only disposable or sanitized character files.

## What to report

Useful reports include:

- arbitrary code execution or unsafe file handling;
- path traversal or unintended file overwrite;
- unsafe temporary-file behavior;
- failures that bypass the Valheim-running write block;
- failures that overwrite a destination before verification succeeds;
- checksum or round-trip verification bypasses;
- backup or atomic-replacement defects;
- packaging defects that load unexpected files or dependencies;
- sensitive data exposure.

## Save files may contain personal data

A `.fch` file can contain character-specific data and may expose names or other information tied to a player's game state. Treat submitted saves as potentially sensitive.

Do not post another person's save file without permission. Prefer a newly created disposable character that reproduces the defect.

## Response priorities

Reports that can destroy or replace a user's save unexpectedly are treated as high priority even if they are not conventional cybersecurity vulnerabilities.

The maintainer will assess:

1. exploitability or corruption risk;
2. whether existing backups/recovery mechanisms contain the impact;
3. affected versions;
4. whether release distribution should pause;
5. the smallest safe remediation and validation plan.

## Disclosure

Please allow reasonable time for investigation and remediation before public disclosure of a sensitive vulnerability. Once a fix is available, the project may publish a concise advisory describing affected versions, impact, and remediation without exposing unnecessary exploit detail.

## Scope boundary

Wulfpack Forge does not provide remote Steam Cloud access and should not request Steam credentials. Any build or third-party distribution asking for Steam credentials should be treated as suspicious.