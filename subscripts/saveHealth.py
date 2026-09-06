import os
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from data.items import CATALOG_GAME_VERSION


SAVE_STATE_VERIFIED = "Verified"
SAVE_STATE_NEEDS_ATTENTION = "Needs attention"
SAVE_STATE_COMPATIBILITY_UNVERIFIED = "Compatibility unverified"

# The current serializer/parser is explicitly configured around character save v43.
# Other versions may still parse, but Wulfpack Forge does not write them until that
# version has its own compatibility evidence.
SUPPORTED_CHARACTER_SAVE_VERSIONS = frozenset({43})


@dataclass(frozen=True)
class SaveHealthReport:
    state: str
    verification_ok: bool
    writable: bool
    save_version: Optional[int]
    source: str
    modified_at: Optional[float]
    catalog_game_version: Optional[str]
    detail: str
    error: Optional[str] = None
    backup_path: Optional[str] = None

    @property
    def save_version_label(self) -> str:
        return f"v{self.save_version}" if self.save_version is not None else "unknown"

    @property
    def modified_label(self) -> str:
        if self.modified_at is None:
            return "unknown"
        try:
            return datetime.fromtimestamp(self.modified_at).strftime("%Y-%m-%d %H:%M")
        except (OSError, OverflowError, ValueError):
            return "unknown"

    @property
    def catalog_label(self) -> str:
        if self.catalog_game_version:
            return f"Valheim {self.catalog_game_version}"
        return "curated fallback"

    @property
    def backup_label(self) -> Optional[str]:
        return os.path.basename(self.backup_path) if self.backup_path else None


def build_save_health_report(
    *,
    valid: bool,
    version: Optional[int],
    source: str,
    modified_at: Optional[float],
    error: Optional[str] = None,
    backup_path: Optional[str] = None,
    catalog_game_version: Optional[str] = CATALOG_GAME_VERSION,
) -> SaveHealthReport:
    source = (source or "Local file").strip() or "Local file"

    if not valid:
        detail = "This file failed strict verification and is not available for editing."
        if error:
            detail += f" {error}"
        return SaveHealthReport(
            state=SAVE_STATE_NEEDS_ATTENTION,
            verification_ok=False,
            writable=False,
            save_version=version,
            source=source,
            modified_at=modified_at,
            catalog_game_version=catalog_game_version,
            detail=detail,
            error=error,
            backup_path=backup_path,
        )

    if version not in SUPPORTED_CHARACTER_SAVE_VERSIONS:
        version_text = "unknown" if version is None else str(version)
        return SaveHealthReport(
            state=SAVE_STATE_COMPATIBILITY_UNVERIFIED,
            verification_ok=True,
            writable=False,
            save_version=version,
            source=source,
            modified_at=modified_at,
            catalog_game_version=catalog_game_version,
            detail=(
                f"Checksum and structure verified, but save version {version_text} is outside "
                "the current write-validated set. You can inspect the character, but Save Changes "
                "is disabled until compatibility is validated."
            ),
            error=None,
            backup_path=backup_path,
        )

    return SaveHealthReport(
        state=SAVE_STATE_VERIFIED,
        verification_ok=True,
        writable=True,
        save_version=version,
        source=source,
        modified_at=modified_at,
        catalog_game_version=catalog_game_version,
        detail=(
            f"Checksum and structure verified. Save version {version} is in the current "
            "write-validated set."
        ),
        error=None,
        backup_path=backup_path,
    )
