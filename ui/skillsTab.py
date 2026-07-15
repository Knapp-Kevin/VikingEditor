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

class SkillsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.player_data = None

        layout = QVBoxLayout(self)

        # add/remove
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
        self.player_data = player_data
        skills = player_data.get("skills", [])
        
        self.table.setRowCount(0)
        for skill in skills:
            self.add_skill_row(skill)

    def add_skill_row(self, skill_data=None):
        row = self.table.rowCount()
        self.table.insertRow(row)

        skill_id = skill_data.get("id", 0) if skill_data else 0
        skill_name = VALHEIM_SKILLS.get(skill_id, f"Unknown ({skill_id})")

        skill_item = QTableWidgetItem(skill_name)
        skill_item.setFlags(skill_item.flags() & ~Qt.ItemIsEditable)
        self.table.setItem(row, 0, skill_item)

        level_spin = QDoubleSpinBox()
        level_spin.setRange(0.0, 100.0)
        level_spin.setDecimals(1)
        level_spin.setValue(skill_data.get("level", 1.0) if skill_data else 1.0)
        self.table.setCellWidget(row, 1, level_spin)

        xp_spin = QDoubleSpinBox()
        xp_spin.setRange(0.0, 999999.0)
        xp_spin.setDecimals(4)
        xp_spin.setValue(skill_data.get("xp", 0.0) if skill_data else 0.0)
        self.table.setCellWidget(row, 2, xp_spin)

    def maximize_all_skills(self):
        for row in range(self.table.rowCount()):
            level_widget = self.table.cellWidget(row, 1)
            if isinstance(level_widget, QDoubleSpinBox):
                level_widget.setValue(100.0)
    
    def set_all_skills0(self):
        for row in range(self.table.rowCount()):
            level_widget = self.table.cellWidget(row, 1)
            if isinstance(level_widget, QDoubleSpinBox):
                level_widget.setValue(0.0)

    def save_changes(self):
        if not self.player_data:
            return

        updated_skills = []

        for row in range(self.table.rowCount()):
            skill_item = self.table.item(row, 0)
            level_widget = self.table.cellWidget(row, 1)
            xp_widget = self.table.cellWidget(row, 2)

            if skill_item and isinstance(level_widget, QDoubleSpinBox) and isinstance(xp_widget, QDoubleSpinBox):
                skill_name = skill_item.text()

                skill_id = next(
                    (id for id, name in VALHEIM_SKILLS.items() if name == skill_name),
                    0
                )

                updated_skills.append({
                    "id": skill_id,
                    "level": level_widget.value(),
                    "xp": xp_widget.value()
                })

        self.player_data["skills"] = updated_skills