import os
import platform
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Optional

from subscripts.saveSafety import SaveVerificationError, verify_fch_round_trip


VALHEIM_APP_ID = "892970"


@dataclass(frozen=True)
class CharacterSave:
    path: str
    name: str
    source: str
    modified_at: float
    version: Optional[int]
    valid: bool
    error: Optional[str] = None

    @property
    def modified_label(self) -> str:
        return datetime.fromtimestamp(self.modified_at).strftime("%Y-%m-%d %H:%M")

    @property
    def display_label(self) -> str:
        status = "" if self.valid else " [needs attention]"
        return f"{self.name} — {self.source} — {self.modified_label}{status}"


def _existing_directories(paths: Iterable[Path]) -> List[Path]:
    found = []
    seen = set()
    for path in paths:
        try:
            resolved = path.expanduser().resolve()
        except OSError:
            continue
        key = os.path.normcase(str(resolved))
        if key not in seen and resolved.is_dir():
            seen.add(key)
            found.append(resolved)
    return found


def _local_save_roots(home: Path, system_name: str) -> List[Path]:
    if system_name == "Windows":
        base = home / "AppData" / "LocalLow" / "IronGate" / "Valheim"
        return [base / "characters_local", base / "characters"]

    if system_name == "Darwin":
        bases = [
            home / "Library" / "Application Support" / "com.coffeestain.Valheim",
            home / "Library" / "Application Support" / "unity.IronGate.Valheim-macOS-Custom",
            home / "Containers" / "Valheim" / "Data" / "Library" / "Application Support" / "com.coffeestain.Valheim",
        ]
        return [child for base in bases for child in (base / "characters_local", base / "characters")]

    base = home / ".config" / "unity3d" / "IronGate" / "Valheim"
    return [base / "characters_local", base / "characters"]


def _steam_userdata_roots(home: Path, system_name: str) -> List[Path]:
    candidates = []

    if system_name == "Windows":
        for env_name in ("PROGRAMFILES(X86)", "PROGRAMFILES"):
            base = os.environ.get(env_name)
            if base:
                candidates.append(Path(base) / "Steam" / "userdata")
        steam_dir = os.environ.get("STEAM_DIR")
        if steam_dir:
            candidates.append(Path(steam_dir) / "userdata")
    elif system_name == "Darwin":
        candidates.append(home / "Library" / "Application Support" / "Steam" / "userdata")
    else:
        candidates.extend([
            home / ".steam" / "steam" / "userdata",
            home / ".local" / "share" / "Steam" / "userdata",
        ])

    return candidates


def candidate_character_directories(
    home: Optional[Path] = None,
    system_name: Optional[str] = None,
) -> List[tuple[Path, str]]:
    home = Path(home or Path.home())
    system_name = system_name or platform.system()

    candidates: List[tuple[Path, str]] = [
        (path, "Local") for path in _local_save_roots(home, system_name)
    ]

    for userdata_root in _existing_directories(_steam_userdata_roots(home, system_name)):
        try:
            account_dirs = [path for path in userdata_root.iterdir() if path.is_dir()]
        except OSError:
            continue

        for account_dir in account_dirs:
            remote = account_dir / VALHEIM_APP_ID / "remote"
            candidates.extend([
                (remote / "characters", "Steam Cloud"),
                (remote / "characters_local", "Steam Local Sync"),
            ])

    found = []
    seen = set()
    for path, source in candidates:
        try:
            resolved = path.expanduser().resolve()
        except OSError:
            continue
        key = os.path.normcase(str(resolved))
        if key in seen or not resolved.is_dir():
            continue
        seen.add(key)
        found.append((resolved, source))
    return found


def inspect_character_save(path: Path, source: str) -> CharacterSave:
    modified_at = path.stat().st_mtime
    fallback_name = path.stem

    try:
        parsed = verify_fch_round_trip(str(path))
        return CharacterSave(
            path=str(path),
            name=(parsed.get("character_name") or fallback_name).strip() or fallback_name,
            source=source,
            modified_at=modified_at,
            version=parsed.get("version"),
            valid=True,
        )
    except (SaveVerificationError, OSError, ValueError, KeyError) as exc:
        return CharacterSave(
            path=str(path),
            name=fallback_name,
            source=source,
            modified_at=modified_at,
            version=None,
            valid=False,
            error=str(exc),
        )


def discover_character_saves(
    home: Optional[Path] = None,
    system_name: Optional[str] = None,
) -> List[CharacterSave]:
    results = []
    seen_files = set()

    for directory, source in candidate_character_directories(home, system_name):
        try:
            files = directory.glob("*.fch")
            for path in files:
                try:
                    resolved = path.resolve()
                except OSError:
                    continue
                key = os.path.normcase(str(resolved))
                if key in seen_files or not resolved.is_file():
                    continue
                seen_files.add(key)
                results.append(inspect_character_save(resolved, source))
        except OSError:
            continue

    results.sort(key=lambda item: (not item.valid, -item.modified_at, item.name.lower()))
    return results
