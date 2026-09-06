"""Render inventory icons: a tinted glyph master when present, else a drawn placeholder."""
from pathlib import Path
from typing import Dict, Optional, Tuple, Union

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QIcon, QImageReader, QPainter, QPixmap

from data.glyphs import GLYPH_IDS, GLYPH_MASTER_DIR, TINTS, glyph_for
from data.items import ItemDefinition, resolve_item
from ui.branding import resource_path

_CACHE: Dict[Tuple[str, str, int], QPixmap] = {}
GLYPH_MASTER_SIZE = 512


def clear_cache() -> None:
    _CACHE.clear()


def master_dir() -> Path:
    return resource_path(GLYPH_MASTER_DIR)


def tint_pixmap(pixmap: QPixmap, color: QColor) -> QPixmap:
    """Multiply the pixmap by ``color`` while keeping its original alpha."""
    result = QPixmap(pixmap.size())
    result.fill(Qt.transparent)
    painter = QPainter(result)
    painter.drawPixmap(0, 0, pixmap)
    painter.setCompositionMode(QPainter.CompositionMode_Multiply)
    painter.fillRect(result.rect(), color)
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return result


def placeholder_pixmap(label: str, color: QColor, size: int) -> QPixmap:
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QColor("#1a1f24"))
    painter.setBrush(color)
    radius = size * 0.18
    painter.drawRoundedRect(QRectF(1, 1, size - 2, size - 2), radius, radius)
    font = QFont()
    font.setBold(True)
    font.setPixelSize(int(size * 0.38))
    painter.setFont(font)
    painter.setPen(QColor("#f4f7f9") if color.lightness() < 150 else QColor("#1a1f24"))
    painter.drawText(pixmap.rect(), Qt.AlignCenter, label)
    painter.end()
    return pixmap


def _label_for(item: Optional[ItemDefinition], prefab: str) -> str:
    words = (item.display_name if item else prefab).replace("_", " ").split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return (words[0][:2] if words else "?").upper()


def item_pixmap(target: Union[str, ItemDefinition], size: int = 64) -> QPixmap:
    item = target if isinstance(target, ItemDefinition) else resolve_item(target)
    prefab = item.prefab if item else str(target)
    glyph, tint = glyph_for(item)
    key = (glyph if item else f"placeholder:{prefab}", tint, size)
    cached = _CACHE.get(key)
    if cached is not None:
        return cached

    color = QColor(TINTS[tint])
    master = master_dir() / f"{glyph}.png"
    if master.is_file() and not QPixmap(str(master)).isNull():
        pixmap = tint_pixmap(
            QPixmap(str(master)).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation), color
        )
    else:
        pixmap = placeholder_pixmap(_label_for(item, prefab), color, size)
    _CACHE[key] = pixmap
    return pixmap


def item_icon(target: Union[str, ItemDefinition], size: int = 64) -> QIcon:
    return QIcon(item_pixmap(target, size))


def glyph_bundle_is_usable() -> bool:
    """Check objective runtime requirements without pretending CI can judge art."""
    if len(GLYPH_IDS) != 23 or len(set(GLYPH_IDS)) != 23:
        return False

    for glyph_id in GLYPH_IDS:
        path = master_dir() / f"{glyph_id}.png"
        if not path.is_file():
            return False
        reader = QImageReader(str(path))
        if not reader.canRead():
            return False
        image = reader.read()
        if (
            image.isNull()
            or image.width() != GLYPH_MASTER_SIZE
            or image.height() != GLYPH_MASTER_SIZE
            or not image.hasAlphaChannel()
        ):
            return False
    return True
