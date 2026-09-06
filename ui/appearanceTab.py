from PySide6.QtWidgets import (
    QWidget,
    QFormLayout,
    QComboBox,
    QPushButton,
    QColorDialog,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
)
from PySide6.QtCore import QSize
from PySide6.QtGui import QColor, QPalette
from data.appearance import BEARD_NONE, HAIR_NONE, VALHEIM_BEARDS, VALHEIM_HAIRS, display_key
from ui.fieldTracker import FieldTracker, select_or_add_unknown
from ui.glyphs import populate_appearance_combo


def _to_qcolor(rgb_list) -> QColor:
    return QColor(*(int(max(0.0, min(1.0, component)) * 255) for component in rgb_list[:3]))


class AppearanceTab(QWidget):
    """Appearance controls; unknown styles are shown as raw entries and never replaced."""

    def __init__(self):
        super().__init__()
        self.player_data = None
        self.tracker = FieldTracker()

        main_layout = QVBoxLayout(self)

        style_group = QGroupBox("Physical Customization")
        style_layout = QFormLayout(style_group)

        self.model_combo = QComboBox()
        self.model_combo.addItem("Male (Model 0)", 0)
        self.model_combo.addItem("Female (Model 1)", 1)

        self.hair_combo = QComboBox()
        self.hair_combo.setIconSize(QSize(48, 48))
        populate_appearance_combo(self.hair_combo, VALHEIM_HAIRS, "hair")

        self.beard_combo = QComboBox()
        self.beard_combo.setIconSize(QSize(48, 48))
        populate_appearance_combo(self.beard_combo, VALHEIM_BEARDS, "beard")

        style_layout.addRow("Gender Model:", self.model_combo)
        style_layout.addRow("Hair Style:", self.hair_combo)
        style_layout.addRow("Beard Style:", self.beard_combo)
        main_layout.addWidget(style_group)

        color_group = QGroupBox("Color Customization")
        color_layout = QHBoxLayout(color_group)

        skin_vbox = QVBoxLayout()
        skin_vbox.addWidget(QLabel("Skin Tone:"))
        self.btn_skin_color = QPushButton("Pick Skin Color")
        self.skin_preview = QWidget()
        self.skin_preview.setFixedSize(100, 30)
        self.skin_preview.setAutoFillBackground(True)
        skin_vbox.addWidget(self.skin_preview)
        skin_vbox.addWidget(self.btn_skin_color)
        color_layout.addLayout(skin_vbox)

        color_layout.addSpacing(40)

        hair_vbox = QVBoxLayout()
        hair_vbox.addWidget(QLabel("Hair/Beard Color:"))
        self.btn_hair_color = QPushButton("Pick Hair Color")
        self.hair_preview = QWidget()
        self.hair_preview.setFixedSize(100, 30)
        self.hair_preview.setAutoFillBackground(True)
        hair_vbox.addWidget(self.hair_preview)
        hair_vbox.addWidget(self.btn_hair_color)
        color_layout.addLayout(hair_vbox)

        main_layout.addWidget(color_group)
        main_layout.addStretch()

        self.current_skin_rgb = [1.0, 1.0, 1.0]
        self.current_hair_rgb = [1.0, 1.0, 1.0]

        self.btn_skin_color.clicked.connect(self.choose_skin_color)
        self.btn_hair_color.clicked.connect(self.choose_hair_color)
        self.model_combo.currentIndexChanged.connect(self.on_model_changed)

    def on_model_changed(self, index):
        # The female model has no beard in game; the stored value is still preserved.
        self.beard_combo.setEnabled(self.model_combo.currentData() == 0)

    def load_data(self, player_data):
        self.tracker.clear()
        self.player_data = player_data
        if not self.player_data:
            return

        select_or_add_unknown(self.model_combo, self.player_data.get("model_index", 0))
        select_or_add_unknown(self.hair_combo, display_key(self.player_data.get("hair", ""), HAIR_NONE))
        select_or_add_unknown(self.beard_combo, display_key(self.player_data.get("beard", ""), BEARD_NONE))
        self.beard_combo.setEnabled(self.model_combo.currentData() == 0)

        self.current_skin_rgb = list(self.player_data.get("skin_color", [1.0, 1.0, 1.0]))
        self.current_hair_rgb = list(self.player_data.get("hair_color", [1.0, 1.0, 1.0]))
        self.update_color_preview(self.skin_preview, self.current_skin_rgb)
        self.update_color_preview(self.hair_preview, self.current_hair_rgb)

        self.tracker.remember("model_index", self.model_combo.currentData())
        self.tracker.remember("hair", self.hair_combo.currentData())
        self.tracker.remember("beard", self.beard_combo.currentData())
        self.tracker.remember("skin_color", list(self.current_skin_rgb))
        self.tracker.remember("hair_color", list(self.current_hair_rgb))

    def update_color_preview(self, widget, rgb_list):
        palette = widget.palette()
        palette.setColor(QPalette.Window, _to_qcolor(rgb_list))
        widget.setPalette(palette)

    def choose_skin_color(self):
        color = QColorDialog.getColor(_to_qcolor(self.current_skin_rgb), self, "Select Skin Color")
        if color.isValid():
            self.current_skin_rgb = [color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0]
            self.update_color_preview(self.skin_preview, self.current_skin_rgb)

    def choose_hair_color(self):
        color = QColorDialog.getColor(_to_qcolor(self.current_hair_rgb), self, "Select Hair/Beard Color")
        if color.isValid():
            self.current_hair_rgb = [color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0]
            self.update_color_preview(self.hair_preview, self.current_hair_rgb)

    def save_changes(self):
        if not self.player_data:
            return

        pending = {
            "model_index": self.model_combo.currentData(),
            "hair": self.hair_combo.currentData(),
            "beard": self.beard_combo.currentData(),
            "skin_color": list(self.current_skin_rgb),
            "hair_color": list(self.current_hair_rgb),
        }
        for key, value in pending.items():
            if self.tracker.changed(key, value):
                self.player_data[key] = value
