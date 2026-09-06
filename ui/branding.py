import sys
from pathlib import Path

from PySide6.QtGui import QImageReader


APP_NAME = "Wulfpack Forge"
APP_SUBTITLE = "Character Editor for Valheim"
APP_AUTHOR = "Frostwulf"
APP_WINDOW_TITLE = f"{APP_NAME} | {APP_SUBTITLE}"
BANNER_RELATIVE_PATH = "assets/wulfpack-forge-banner.jpg"
MIN_BANNER_WIDTH = 800
MIN_BANNER_HEIGHT = 250


def resource_path(relative_path: str) -> Path:
    """Resolve a repository resource in source runs and PyInstaller bundles."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / relative_path
    return Path(__file__).resolve().parents[1] / relative_path


def banner_path() -> Path:
    return resource_path(BANNER_RELATIVE_PATH)


def banner_is_usable() -> bool:
    """Verify the approved banner exists, decodes, and has banner-scale dimensions."""
    path = banner_path()
    if not path.is_file():
        return False

    reader = QImageReader(str(path))
    if not reader.canRead():
        return False

    size = reader.size()
    return size.width() >= MIN_BANNER_WIDTH and size.height() >= MIN_BANNER_HEIGHT
