# Support

Wulfpack Forge is community software. Support is provided through this repository on a best-effort basis.

## Before opening an issue

Check the following first:

1. **Close Valheim.** Wulfpack Forge intentionally blocks writes while the game is running.
2. **Confirm the character exists locally.** Steam Cloud characters must be synchronized to the computer before Wulfpack Forge can discover them.
3. **Click Refresh.** The character list only reflects files currently visible on disk.
4. **Try Browse for Another Save.** If you already know where the `.fch` file is, open it directly.
5. **Keep the original backup.** Do not delete timestamped `.bak` files while investigating a save problem.
6. **Check compatibility status.** Major Valheim updates may require explicit revalidation before Wulfpack Forge is considered compatible.

## Steam Cloud characters

Wulfpack Forge does not read remote Steam Cloud storage directly.

If a character is visible on another machine but not this one, allow Steam to synchronize it locally. Launch Valheim to confirm the character appears, exit the game, then refresh Wulfpack Forge.

Do not provide your Steam password or authentication tokens to Wulfpack Forge or to anyone claiming they are required for support.

## What to include in a bug report

Please include:

- Wulfpack Forge version or commit;
- Valheim version;
- Windows version if relevant;
- whether the character is local, Steam-synchronized, or modded;
- the action you attempted;
- what you expected;
- what happened instead;
- exact error text when available.

For UI problems, screenshots are useful. For save-format problems, use a disposable or sanitized character whenever possible.

## Save files

Do not upload a valuable primary character unless absolutely necessary. Prefer reproducing the issue with a newly created disposable character.

If a save operation failed, preserve:

- the original `.fch`;
- any timestamped `.bak` created by Wulfpack Forge;
- the error message;
- the Valheim build number.

## Feature requests

Feature requests belong in GitHub Issues. Describe the player problem first, then the proposed solution. The durable product roadmap is tracked in [issue #2](https://github.com/Knapp-Kevin/WulfPackForge/issues/2).

## Not supported

The project does not promise support for:

- every modded save format or mod interaction;
- unreleased Valheim builds;
- direct remote Steam Cloud access;
- live-memory editing;
- unofficial third-party builds that differ from this repository;
- recovery of every historically corrupted save.

## Security issues

For sensitive vulnerabilities, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.