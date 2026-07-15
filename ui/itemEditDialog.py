from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QCheckBox,
    QDialogButtonBox
)

class ItemEditDialog(QDialog):
    """A dialog to edit details of a specific item slot."""
    def __init__(self, item_data, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Inventory Item")
        self.item_data = item_data

        layout = QFormLayout(self)

        self.prefab_input = QLineEdit(item_data.get("prefab", ""))
        self.stack_input = QSpinBox()
        self.stack_input.setRange(1, 9999)
        self.stack_input.setValue(item_data.get("stack", 1))

        self.durability_input = QDoubleSpinBox()
        self.durability_input.setRange(0.0, 99999.0)
        self.durability_input.setValue(item_data.get("durability", 100.0))

        self.quality_input = QSpinBox()
        self.quality_input.setRange(1, 5)
        self.quality_input.setValue(item_data.get("quality", 1))

        self.variant_input = QSpinBox()
        self.variant_input.setRange(0, 99)
        self.variant_input.setValue(item_data.get("variant", 0))

        self.equipped_input = QCheckBox()
        self.equipped_input.setChecked(item_data.get("equipped", False))

        layout.addRow("Prefab ID:", self.prefab_input)
        layout.addRow("Stack Size:", self.stack_input)
        layout.addRow("Durability:", self.durability_input)
        layout.addRow("Quality Level:", self.quality_input)
        layout.addRow("Variant (Style):", self.variant_input)
        layout.addRow("Equipped:", self.equipped_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)

    def get_updated_data(self):
        return {
            "prefab": self.prefab_input.text().strip(),
            "stack": self.stack_input.value(),
            "durability": self.durability_input.value(),
            "quality": self.quality_input.value(),
            "variant": self.variant_input.value(),
            "equipped": self.equipped_input.isChecked()
        }
