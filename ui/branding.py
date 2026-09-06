import struct
import sys
from pathlib import Path
from typing import Optional, Tuple


APP_NAME = "Wulfpack Forge"
APP_SUBTITLE = "Character Editor for Valheim"
APP_AUTHOR = "Frostwulf"
APP_WINDOW_TITLE = f"{APP_NAME} | {APP_SUBTITLE}"
BANNER_RELATIVE_PATH = "assets/wulfpack-forge-banner.jpg"
MIN_BANNER_WIDTH = 1200
MIN_BANNER_HEIGHT = 400
MIN_BANNER_BYTES = 12_000


# JPEG Start-of-Frame markers that carry image dimensions.
_JPEG_SOF_MARKERS = {
    0xC0,
    0xC1,
    0xC2,
    0xC3,
    0xC5,
    0xC6,
    0xC7,
    0xC9,
    0xCA,
    0xCB,
    0xCD,
    0xCE,
    0xCF,
}


def resource_path(relative_path: str) -> Path:
    """Resolve a repository resource in source runs and PyInstaller bundles."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / relative_path
    return Path(__file__).resolve().parents[1] / relative_path


def banner_path() -> Path:
    return resource_path(BANNER_RELATIVE_PATH)


def _jpeg_dimensions(path: Path) -> Optional[Tuple[int, int]]:
    """Return JPEG dimensions without depending on Qt image plugins.

    Qt still renders the banner in the UI, but CI and packaged smoke tests should
    not fail just because a Linux runner is missing a JPEG reader plugin.
    """
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None

        while True:
            byte = handle.read(1)
            if not byte:
                return None
            if byte != b"\xff":
                continue

            marker_byte = handle.read(1)
            while marker_byte == b"\xff":
                marker_byte = handle.read(1)
            if not marker_byte:
                return None

            marker = marker_byte[0]
            if marker in (0xD8, 0xD9):
                continue
            if marker == 0xDA:
                return None

            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None
            segment_length = struct.unpack(">H", length_bytes)[0]
            if segment_length < 2:
                return None

            if marker in _JPEG_SOF_MARKERS:
                data = handle.read(segment_length - 2)
                if len(data) < 5:
                    return None
                height, width = struct.unpack(">HH", data[1:5])
                return width, height

            handle.seek(segment_length - 2, 1)


def banner_is_usable() -> bool:
    """Verify the approved banner is a readable, README-scale runtime asset."""
    path = banner_path()
    if not path.is_file() or path.stat().st_size < MIN_BANNER_BYTES:
        return False

    dimensions = _jpeg_dimensions(path)
    if dimensions is None:
        return False

    width, height = dimensions
    return width >= MIN_BANNER_WIDTH and height >= MIN_BANNER_HEIGHT
