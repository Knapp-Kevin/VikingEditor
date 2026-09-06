import sys
from pathlib import Path


APP_NAME = "Wulfpack Forge"
APP_SUBTITLE = "Character Editor for Valheim"
APP_AUTHOR = "Frostwulf"
APP_WINDOW_TITLE = f"{APP_NAME} | {APP_SUBTITLE}"
BANNER_RELATIVE_PATH = "assets/wulfpack-forge-banner.jpg"


def resource_path(relative_path: str) -> Path:
    """Resolve a repository resource in source runs and PyInstaller bundles."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / relative_path
    return Path(__file__).resolve().parents[1] / relative_path


def banner_path() -> Path:
    return resource_path(BANNER_RELATIVE_PATH)
