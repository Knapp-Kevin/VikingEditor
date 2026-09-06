from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QPushButton

from data.items import resolve_item
from ui.glyphs import item_icon


class InventorySlot(QPushButton):
    """A visual representation of a single Valheim inventory grid tile."""

    def __init__(self, x, y, parent=None):
        super().__init__(parent)
        self.grid_x = x
        self.grid_y = y
        self.item_data = None
        self.setFixedSize(90, 90)
        self.update_visuals()

    def set_item(self, item_data):
        self.item_data = item_data
        self.update_visuals()

    def clear_item(self):
        self.item_data = None
        self.update_visuals()

    def update_visuals(self):
        if self.item_data:
            prefab = self.item_data.get("prefab", "Unknown")
            stack = self.item_data.get("stack", 1)
            is_equipped = self.item_data.get("equipped", False)
            catalog_item = resolve_item(prefab)
            display_name = (
                catalog_item.display_name
                if catalog_item
                else prefab.replace("$item_", "").replace("_", " ").title()
            )

            equipped_marker = "\n[ EQUIPPED ]" if is_equipped else ""
            self.setIcon(item_icon(prefab, 40))
            self.setIconSize(QSize(40, 40))
            self.setText(f"{display_name}\nx{stack}{equipped_marker}")
            self.setToolTip(
                f"Prefab: {prefab}\n"
                f"Quality: {self.item_data.get('quality', 1)}\n"
                f"Variant: {self.item_data.get('variant', 0)}"
            )

            if is_equipped:
                self.setStyleSheet(
                    "background-color: #556B2F; color: white; "
                    "border: 2px solid #9acd32; font-weight: bold;"
                )
            else:
                self.setStyleSheet(
                    "background-color: #3e2723; color: #d7ccc8; border: 1px solid #5d4037;"
                )
        else:
            self.setIcon(QIcon())
            self.setText(f"({self.grid_x}, {self.grid_y})")
            self.setToolTip("Empty inventory slot")
            self.setStyleSheet(
                "background-color: #1a1a1a; color: #444444; border: 1px dashed #333333;"
            )
