import json
import os
import tempfile

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import *

from ui.inventoryTab import InventoryTab
from ui.skillsTab import SkillsTab
from ui.statsTab import StatsTab
from ui.appearanceTab import AppearanceTab
from ui.miscTab import MiscTab
from ui.valheim_detection import is_valheim_running, valheim_warning_message
from ui.branding import APP_NAME, APP_SUBTITLE, APP_AUTHOR, APP_WINDOW_TITLE, banner_path

from subscripts.characterDiscovery import discover_character_saves
from subscripts.fchUtil import compile_fch
from subscripts.saveSafety import replace_verified_save, verify_fch_round_trip

from subscripts.playerDataUtil import (
    unpack_player_data_hex,
    pack_player_data_hex
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if is_valheim_running():
            warning_msg = valheim_warning_message()
            msg = QMessageBox(self)
            msg.setWindowTitle("Valheim Running")
            msg.setText(warning_msg)
            msg.setInformativeText(
                "You can inspect a character while Valheim is open, but saving is blocked until the game is closed."
            )
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

        self.root_save = None
        self.player_data = None
        self.current_fch = None
        self.discovered_characters = []

        self.setWindowTitle(APP_WINDOW_TITLE)
        self.resize(1200, 900)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(10)

        self._brand_pixmap = QPixmap(str(banner_path()))
        self.brand_banner = QLabel()
        self.brand_banner.setObjectName("brandBanner")
        self.brand_banner.setFixedHeight(180)
        self.brand_banner.setAlignment(Qt.AlignCenter)
        self.brand_banner.setAccessibleName(f"{APP_NAME} banner")
        self.brand_banner.setAccessibleDescription(
            f"{APP_NAME}, {APP_SUBTITLE}, by {APP_AUTHOR}."
        )
        self.brand_banner.setStyleSheet(
            "QLabel#brandBanner { background-color: #07151c; border-radius: 8px; }"
        )
        main_layout.addWidget(self.brand_banner)
        self._refresh_brand_banner()

        intro = QLabel(
            "Choose your character, make changes in the tabs below, then click Save Changes. "
            "Existing saves are backed up and verified automatically."
        )
        intro.setWordWrap(True)
        main_layout.addWidget(intro)

        discovery_layout = QHBoxLayout()
        self.character_combo = QComboBox()
        self.character_combo.setMinimumWidth(420)
        self.character_combo.setToolTip(
            "Verified Valheim character files found on this computer, including local copies synchronized by Steam Cloud."
        )
        self.btn_refresh_characters = QPushButton("Refresh")
        self.btn_open_discovered = QPushButton("Open Character")
        discovery_layout.addWidget(QLabel("Character:"))
        discovery_layout.addWidget(self.character_combo, 1)
        discovery_layout.addWidget(self.btn_refresh_characters)
        discovery_layout.addWidget(self.btn_open_discovered)
        main_layout.addLayout(discovery_layout)

        self.discovery_help = QLabel()
        self.discovery_help.setWordWrap(True)
        self.discovery_help.setVisible(False)
        main_layout.addWidget(self.discovery_help)

        button_layout = QHBoxLayout()
        self.btn_open_save = QPushButton("Browse for Another Save")
        self.btn_save_save = QPushButton("Save Changes")
        self.btn_save_save.setEnabled(False)
        button_layout.addWidget(self.btn_open_save)
        button_layout.addStretch(1)
        button_layout.addWidget(self.btn_save_save)
        main_layout.addLayout(button_layout)

        self.file_label = QLabel("No character loaded")
        main_layout.addWidget(self.file_label)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.inventory_tab = InventoryTab()
        self.skills_tab = SkillsTab()
        self.stats_tab = StatsTab()
        self.appearance_tab = AppearanceTab()
        self.misc_tab = MiscTab()

        self.tabs.addTab(self.appearance_tab, "Appearance")
        self.tabs.addTab(self.inventory_tab, "Inventory")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.misc_tab, "Misc")

        self.btn_refresh_characters.clicked.connect(self.refresh_discovered_characters)
        self.btn_open_discovered.clicked.connect(self.open_selected_character)
        self.character_combo.activated.connect(lambda _index: self._update_character_tooltip())
        self.btn_open_save.clicked.connect(self.open_save_file)
        self.btn_save_save.clicked.connect(self.save_save_file)

        self.refresh_discovered_characters()

    def _refresh_brand_banner(self):
        if self._brand_pixmap.isNull():
            self.brand_banner.setText(f"{APP_NAME}\n{APP_SUBTITLE}\nby {APP_AUTHOR}")
            return

        target = self.brand_banner.size()
        if target.width() <= 0 or target.height() <= 0:
            return

        scaled = self._brand_pixmap.scaled(
            target,
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        x = max(0, (scaled.width() - target.width()) // 2)
        y = max(0, (scaled.height() - target.height()) // 2)
        cropped = scaled.copy(x, y, target.width(), target.height())
        self.brand_banner.setPixmap(cropped)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "brand_banner"):
            self._refresh_brand_banner()

    def refresh_discovered_characters(self):
        previous_path = self.current_fch
        self.discovered_characters = discover_character_saves()
        self.character_combo.clear()

        if not self.discovered_characters:
            self.character_combo.addItem("No local Valheim character files found", None)
            self.btn_open_discovered.setEnabled(False)
            self.character_combo.setToolTip(
                "Wulfpack Forge can only open character files that exist on this computer."
            )
            self.discovery_help.setText(
                "No local character files were found. If this character is stored in Steam Cloud, "
                "make sure Steam has synchronized it to this computer and that Valheim can see it locally, "
                "then click Refresh. Wulfpack Forge does not download saves directly from Steam Cloud. "
                "Use Browse for Another Save if you already have the .fch file elsewhere."
            )
            self.discovery_help.setVisible(True)
            return

        self.discovery_help.setVisible(False)
        selected_index = 0
        for index, character in enumerate(self.discovered_characters):
            self.character_combo.addItem(character.display_label, character.path)
            if previous_path and os.path.normcase(character.path) == os.path.normcase(previous_path):
                selected_index = index

        self.character_combo.setCurrentIndex(selected_index)
        self.btn_open_discovered.setEnabled(True)
        self._update_character_tooltip()

    def _update_character_tooltip(self):
        index = self.character_combo.currentIndex()
        if index < 0 or index >= len(self.discovered_characters):
            return

        character = self.discovered_characters[index]
        details = [
            f"Path: {character.path}",
            f"Source: {character.source}",
            f"Modified: {character.modified_label}",
        ]
        if character.version is not None:
            details.append(f"Save version: {character.version}")
        if character.error:
            details.append(f"Validation: {character.error}")
        else:
            details.append("Validation: checksum and structure verified")
        self.character_combo.setToolTip("\n".join(details))

    def open_selected_character(self):
        filename = self.character_combo.currentData()
        if filename:
            self.load_save_file(filename)

    def load_save_file(self, filename):
        try:
            root_save = verify_fch_round_trip(filename)
            player_hex = root_save.get("player_data_hex")
            if not player_hex:
                QMessageBox.warning(
                    self,
                    "Character Has No Player Data",
                    "The save container is valid, but it contains no editable player data."
                )
                return

            player_data = unpack_player_data_hex(player_hex)

            self.root_save = root_save
            self.player_data = player_data
            self.current_fch = filename

            self.inventory_tab.load_data(self.player_data)
            self.skills_tab.load_data(self.player_data)
            self.stats_tab.load_data(self.player_data, self.root_save)
            self.appearance_tab.load_data(self.player_data)
            self.misc_tab.load_data(self.player_data, self.root_save)

            self.file_label.setText(
                f"Editing: {self.root_save.get('character_name')}  •  {os.path.basename(filename)}"
            )
            self.btn_save_save.setEnabled(True)
            self.tabs.setCurrentWidget(self.appearance_tab)
            self.refresh_discovered_characters()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Character Could Not Be Opened",
                "This save was not loaded because it could not be verified and parsed safely."
                f"\n\n{str(e)}"
            )

    def open_save_file(self):
        initial_dir = os.path.dirname(self.current_fch) if self.current_fch else ""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Valheim Character Save",
            initial_dir,
            "Valheim Character (*.fch)"
        )
        if filename:
            self.load_save_file(filename)

    def _block_save_if_valheim_running(self) -> bool:
        if not is_valheim_running():
            return False

        QMessageBox.critical(
            self,
            "Close Valheim Before Saving",
            f"{valheim_warning_message()}\n\n{APP_NAME} will not write a character save while Valheim is running."
        )
        return True

    def save_save_file(self):
        """Pack, verify, back up, and safely replace the active Valheim save."""
        if not self.root_save or not self.player_data:
            QMessageBox.warning(self, "No Character Loaded", "Open a character before saving changes.")
            return

        if self._block_save_if_valheim_running():
            return

        temp_wrapper_path = None
        candidate_path = None

        try:
            self.inventory_tab.save_changes()
            self.skills_tab.save_changes()
            self.stats_tab.save_changes()
            self.appearance_tab.save_changes()
            self.misc_tab.save_changes()

            char_name = self.root_save.get("character_name", "Viking").strip()
            suggested_filename = f"{char_name.lower()}.fch"

            default_dir = os.path.dirname(self.current_fch) if self.current_fch else ""
            default_save_path = os.path.join(default_dir, suggested_filename)

            filename, _ = QFileDialog.getSaveFileName(
                self,
                "Save Character Changes",
                default_save_path,
                "Valheim Character (*.fch)"
            )
            if not filename:
                return

            if self._block_save_if_valheim_running():
                return

            updated_hex_payload = pack_player_data_hex(self.player_data)
            self.root_save["player_data_hex"] = updated_hex_payload

            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".json",
                prefix="wulfpack-forge-",
                delete=False
            ) as wrapper_file:
                json.dump(self.root_save, wrapper_file, indent=4, ensure_ascii=False)
                temp_wrapper_path = wrapper_file.name

            destination_dir = os.path.dirname(os.path.abspath(filename))
            with tempfile.NamedTemporaryFile(
                suffix=".fch",
                prefix=".wulfpack-forge-",
                dir=destination_dir,
                delete=False
            ) as candidate_file:
                candidate_path = candidate_file.name

            compile_fch(temp_wrapper_path, candidate_path)

            backup_path = replace_verified_save(
                candidate_path,
                filename,
                expected_root=self.root_save
            )
            candidate_path = None

            success_text = f"Changes saved safely to:\n{filename}"
            if backup_path:
                success_text += f"\n\nPrevious save backed up to:\n{backup_path}"
            success_text += "\n\nThe new save passed checksum and round-trip verification."

            QMessageBox.information(self, "Changes Saved", success_text)
            self.current_fch = filename
            self.refresh_discovered_characters()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Changes Were Not Saved",
                "The existing destination was not replaced unless verification completed successfully."
                f"\n\n{str(e)}"
            )
        finally:
            for temp_path in (temp_wrapper_path, candidate_path):
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass
