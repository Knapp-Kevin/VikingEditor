"""Categorised item picker: curated groups on the left, an icon grid on the right."""
from typing import Optional

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from data.item_groups import GROUPS, items_in_group, pickable_items
from ui.glyphs import item_icon

ADVANCED = "Advanced"
ICON_SIZE = 64


class ItemPickerDialog(QDialog):
    """Pick a catalog item by category or search, or type a raw prefab under Advanced."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Item")
        self.resize(820, 520)
        self.selected_prefab: Optional[str] = None
        self._current_group = GROUPS[0]

        layout = QHBoxLayout(self)

        self.categories = QListWidget()
        self.categories.setFixedWidth(170)
        for name in GROUPS:
            self.categories.addItem(name)
        self.categories.addItem(ADVANCED)
        layout.addWidget(self.categories)

        right = QVBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search all items by name or prefab")
        right.addWidget(self.search)

        self.pages = QStackedWidget()
        self.grid = QListWidget()
        self.grid.setViewMode(QListWidget.IconMode)
        self.grid.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.grid.setGridSize(QSize(120, 104))
        self.grid.setResizeMode(QListWidget.Adjust)
        self.grid.setWrapping(True)
        self.grid.setUniformItemSizes(True)
        self.grid.setWordWrap(True)
        self.pages.addWidget(self.grid)

        advanced = QWidget()
        advanced_layout = QVBoxLayout(advanced)
        advanced_layout.addWidget(QLabel(
            "Enter a raw prefab ID for a modded item or an item newer than the bundled catalog. "
            "The value is written exactly as typed."
        ))
        self.raw_input = QLineEdit()
        self.raw_input.setPlaceholderText("Prefab ID")
        advanced_layout.addWidget(self.raw_input)
        advanced_layout.addStretch()
        self.pages.addWidget(advanced)
        right.addWidget(self.pages, 1)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        right.addWidget(self.buttons)
        layout.addLayout(right, 1)

        self.categories.currentTextChanged.connect(self.select_group)
        self.search.textChanged.connect(self._apply_search)
        self.grid.itemDoubleClicked.connect(lambda _item: self.accept())
        self.categories.setCurrentRow(0)

    def select_group(self, name: str) -> None:
        if name == ADVANCED:
            self.pages.setCurrentIndex(1)
            self.raw_input.setFocus()
            return
        self._current_group = name
        self.pages.setCurrentIndex(0)
        if self.search.text().strip():
            self._apply_search(self.search.text())
        else:
            self._fill(items_in_group(name))

    def _apply_search(self, text: str) -> None:
        needle = text.strip().lower()
        if not needle:
            self._fill(items_in_group(self._current_group))
            return
        if self.pages.currentIndex() != 0:
            self.pages.setCurrentIndex(0)
        matches = [
            item for item in pickable_items()
            if needle in item.display_name.lower() or needle in item.prefab.lower()
        ]
        self._fill(matches)

    def _fill(self, items) -> None:
        self.grid.clear()
        for item in items:
            row = QListWidgetItem(item_icon(item, ICON_SIZE), item.display_name)
            row.setData(Qt.UserRole, item.prefab)
            row.setToolTip(f"{item.display_name}\nPrefab: {item.prefab}\nType: {item.item_type or 'unknown'}")
            row.setSizeHint(QSize(112, 100))
            self.grid.addItem(row)

    def accept(self) -> None:
        if self.pages.currentIndex() == 1:
            raw = self.raw_input.text().strip()
            if not raw:
                return
            self.selected_prefab = raw
        else:
            current = self.grid.currentItem()
            if current is None:
                return
            self.selected_prefab = current.data(Qt.UserRole)
        super().accept()
