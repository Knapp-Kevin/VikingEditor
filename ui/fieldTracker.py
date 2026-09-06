"""Helpers that let editor tabs write back only what the player changed."""
from PySide6.QtCore import Qt

UNKNOWN_MARKER_ROLE = Qt.UserRole + 1
UNKNOWN_MARKER = "unknown"


class FieldTracker:
    """Remember what a widget reported right after load; report only real changes."""

    def __init__(self):
        self._loaded: dict = {}

    def clear(self) -> None:
        self._loaded.clear()

    def remember(self, key, value) -> None:
        self._loaded[key] = value

    def changed(self, key, value) -> bool:
        return key not in self._loaded or self._loaded[key] != value


def select_or_add_unknown(combo, value) -> None:
    """Select ``value`` in ``combo``, adding a raw "Unknown" entry when it is not a known choice.

    Entries added for a previous character are removed first so an unknown value
    can never leak into a character that did not have it.
    """
    for index in reversed(range(combo.count())):
        if combo.itemData(index, UNKNOWN_MARKER_ROLE) == UNKNOWN_MARKER:
            combo.removeItem(index)

    index = combo.findData(value)
    if index == -1:
        combo.addItem(f"Unknown ({value})", value)
        index = combo.count() - 1
        combo.setItemData(index, UNKNOWN_MARKER, UNKNOWN_MARKER_ROLE)
    combo.setCurrentIndex(index)
