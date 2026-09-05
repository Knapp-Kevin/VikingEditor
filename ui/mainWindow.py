import json
import os
import tempfile

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt

from ui.inventoryTab import InventoryTab
from ui.skillsTab import SkillsTab
from ui.statsTab import StatsTab
from ui.appearanceTab import AppearanceTab
from ui.miscTab import MiscTab
from ui.valheim_detection import is_valheim_running, valheim_warning_message

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
            msg.setWindowTitle("Valheim Running Warning")
            msg.setText(warning_msg)
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec()

        self.root_save = None
        self.player_data = None
        self.current_fch = None
        self.discovered_characters = []

        self.setWindowTitle("Viking Editor")
        self.resize(1200, 800)

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)

        discovery_layout = QHBoxLayout()
        self.character_combo = QComboBox()
        self.character_combo.setMinimumWidth(420)
        self.character_combo.setToolTip(
            "Verified Valheim character saves discovered from local and Steam Cloud locations."
        )
        self.btn_refresh_characters = QPushButton("Refresh Characters")
        self.btn_open_discovered = QPushButton("Open Selected")
        discovery_layout.addWidget(QLabel("Character:"))
        discovery_layout.addWidget(self.character_combo, 1)
        discovery_layout.addWidget(self.btn_refresh_characters)
        discovery_layout.addWidget(self.btn_open_discovered)
        main_layout.addLayout(discovery_layout)

        button_layout = QHBoxLayout()
        self.btn_open_save = QPushButton("Browse for .fch")
        self.btn_open_json = QPushButton("Open JSON")
        self.btn_save_json = QPushButton("Save JSON")
        self.btn_save_save = QPushButton("Save Savefile")

        button_layout.addWidget(self.btn_open_save)
        button_layout.addWidget(self.btn_open_json)
        button_layout.addWidget(self.btn_save_json)
        button_layout.addWidget(self.btn_save_save)
        main_layout.addLayout(button_layout)

        self.file_label = QLabel("No file loaded")
        main_layout.addWidget(self.file_label)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.inventory_tab = InventoryTab()
        self.skills_tab = SkillsTab()
        self.stats_tab = StatsTab()
        self.appearance_tab = AppearanceTab()
        self.misc_tab = MiscTab()

        self.tabs.addTab(self.inventory_tab, "Inventory")
        self.tabs.addTab(self.skills_tab, "Skills")
        self.tabs.addTab(self.stats_tab, "Stats")
        self.tabs.addTab(self.appearance_tab, "Appearance")
        self.tabs.addTab(self.misc_tab, "Misc")

        self.btn_refresh_characters.clicked.connect(self.refresh_discovered_characters)
        self.btn_open_discovered.clicked.connect(self.open_selected_character)
        self.character_combo.activated.connect(lambda _index: self._update_character_tooltip())
        self.btn_open_save.clicked.connect(self.open_save_file)
        self.btn_open_json.clicked.connect(self.open_json_file)
        self.btn_save_json.clicked.connect(self.save_json_file)
        self.btn_save_save.clicked.connect(self.save_save_file)

        self.refresh_discovered_characters()

        try:
            with open("info.txt", "r", encoding="utf-8") as f:
                info_text = f.read()

            msg = QMessageBox(self)
            msg.setWindowTitle("Information")
            msg.setText(info_text)
            msg.setTextFormat(Qt.TextFormat.RichText)
            msg.setTextInteractionFlags(Qt.TextInteractionFlag.TextBrowserInteraction)
            msg.exec()

        except Exception as e:
            QMessageBox.warning(
                self,
                "Info Load Error",
                f"Could not load info.txt:\n{str(e)}\nPlease read the info.txt file manually for important information!"
            )

    def refresh_discovered_characters(self):
        previous_path = self.current_fch
        self.discovered_characters = discover_character_saves()
        self.character_combo.clear()

        if not self.discovered_characters:
            self.character_combo.addItem("No Valheim character saves discovered", None)
            self.btn_open_discovered.setEnabled(False)
            self.character_combo.setToolTip(
                "No saves were found automatically. Use 'Browse for .fch' for a custom location."
            )
            return

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
        if not filename:
            return
        self.load_save_file(filename)

    def load_save_file(self, filename):
        try:
            self.root_save = verify_fch_round_trip(filename)
            self.current_fch = filename

            player_hex = self.root_save.get("player_data_hex")
            if player_hex:
                self.player_data = unpack_player_data_hex(player_hex)
                self.inventory_tab.load_data(self.player_data)
                self.skills_tab.load_data(self.player_data)
                self.stats_tab.load_data(self.player_data, self.root_save)
                self.appearance_tab.load_data(self.player_data)
                self.misc_tab.load_data(self.player_data, self.root_save)

                self.file_label.setText(
                    f"Loaded Save: {os.path.basename(filename)} "
                    f"(Char: {self.root_save.get('character_name')})"
                )
                QMessageBox.information(
                    self,
                    "Character Loaded",
                    "Valheim save checksum and structure verified, then loaded successfully."
                )
                self.refresh_discovered_characters()
            else:
                QMessageBox.warning(
                    self,
                    "Empty Save",
                    "The save container is valid, but it contains no player data."
                )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Character Load Failed",
                "Viking Editor refused to load this save because it could not be verified and parsed safely."
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

    def open_json_file(self):
        QMessageBox.information(
            self,
            "Feature WIP",
            "Opening JSON files is currently a work in progress and not yet implemented."
        )

    def save_json_file(self):
        QMessageBox.information(
            self,
            "Feature WIP",
            "Saving to JSON files is currently a work in progress and not yet implemented."
        )

    def _block_save_if_valheim_running(self) -> bool:
        if not is_valheim_running():
            return False

        QMessageBox.critical(
            self,
            "Save Blocked: Valheim Is Running",
            f"{valheim_warning_message()}\n\nViking Editor will not write a character save while Valheim is running."
        )
        return True

    def save_save_file(self):
        """Pack, verify, back up, and safely replace the active Valheim save."""
        if not self.root_save or not self.player_data:
            QMessageBox.warning(self, "No Save Loaded", "Please load a valid .fch save file first.")
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
                "Compile and Verify Valheim Save",
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
                prefix="vikingeditor-",
                delete=False
            ) as wrapper_file:
                json.dump(self.root_save, wrapper_file, indent=4, ensure_ascii=False)
                temp_wrapper_path = wrapper_file.name

            destination_dir = os.path.dirname(os.path.abspath(filename))
            with tempfile.NamedTemporaryFile(
                suffix=".fch",
                prefix=".vikingeditor-",
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

            success_text = (
                "Character save compiled, checksum-verified, reparsed, and saved successfully!"
                f"\n\nLocation:\n{filename}"
            )
            if backup_path:
                success_text += f"\n\nBackup created:\n{backup_path}"

            QMessageBox.information(self, "Verified Save Complete", success_text)
            self.current_fch = filename
            self.refresh_discovered_characters()

        except Exception as e:
            QMessageBox.critical(
                self,
                "Verified Save Failed",
                "The destination save was not replaced unless verification completed successfully."
                f"\n\n{str(e)}"
            )
        finally:
            for temp_path in (temp_wrapper_path, candidate_path):
                if temp_path and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except OSError:
                        pass
