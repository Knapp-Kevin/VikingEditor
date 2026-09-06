from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QDoubleSpinBox,
    QHeaderView
)

from PySide6.QtCore import Qt

from data.skills import VALHEIM_SKILLS
from ui.fieldTracker import FieldTracker


class SkillsTab(QWidget):
    """Skill rows keep a reference to their payload entry; only edited values are written back."""

    def __init__(self):
        super().__init__()
        self.player_data = None
        self.tracker = FieldTracker()

        layout = QVBoxLayout(self)

        toolbar = QHBoxLayout()
        self.btn_max_all = QPushButton("Maximize All (Lvl 100)")
        self.btn_set_all0 = QPushButton("Set All to 0")
        toolbar.addWidget(self.btn_max_all)
        toolbar.addWidget(self.btn_set_all0)
        toolbar.addStretch()
        layout.addLayout(toolbar)

        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Skill Name", "Level (0-100)", "XP Accumulator"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)
        self.btn_max_all.clicked.connect(self.maximize_all_skills)
        self.btn_set_all0.clicked.connect(self.set_all_skills0)

    def load_data(self, player_data):
        self.tracker.clear()
        self.player_data = player_data
        self.table.setRowCount(0)
        for index, skill in enumerate(player_data.get("skills", [])):
            self.add_skill_row(index, skill)

    def add_skill_row(self, index, skill_data):
        row = self.table.rowCount()
        self.table.insertRow(row)

        skill_id = skill_data.get("id", 0)
        skill_item = QTableWidgetItem(VALHEIM_SKILLS.get(skill_id, f"Unknown ({skill_id})"))
        skill_item.setFlags(skill_item.flags() & ~Qt.ItemIsEditable)
        skill_item.setData(Qt.UserRole, index)
        self.table.setItem(row, 0, skill_item)

        level_spin = QDoubleSpinBox()
        level_spin.setRange(0.0, 100.0)
        level_spin.setDecimals(2)
        level_spin.setValue(skill_data.get("level", 1.0))
        self.table.setCellWidget(row, 1, level_spin)

        xp_spin = QDoubleSpinBox()
        xp_spin.setRange(0.0, 999999.0)
        xp_spin.setDecimals(4)
        xp_spin.setValue(skill_data.get("xp", 0.0))
        self.table.setCellWidget(row, 2, xp_spin)

        self.tracker.remember(("level", index), level_spin.value())
        self.tracker.remember(("xp", index), xp_spin.value())

    def maximize_all_skills(self):
        for row in range(self.table.rowCount()):
            self.table.cellWidget(row, 1).setValue(100.0)

    def set_all_skills0(self):
        for row in range(self.table.rowCount()):
            self.table.cellWidget(row, 1).setValue(0.0)

    def save_changes(self):
        if not self.player_data:
            return

        skills = self.player_data.get("skills", [])
        for row in range(self.table.rowCount()):
            index = self.table.item(row, 0).data(Qt.UserRole)
            if index is None or index >= len(skills):
                continue
            level = self.table.cellWidget(row, 1).value()
            xp = self.table.cellWidget(row, 2).value()
            if self.tracker.changed(("level", index), level):
                skills[index]["level"] = level
            if self.tracker.changed(("xp", index), xp):
                skills[index]["xp"] = xp
