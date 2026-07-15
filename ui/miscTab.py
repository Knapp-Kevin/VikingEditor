from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QFormLayout, QLineEdit

class MiscTab(QWidget):
    def __init__(self):
        super().__init__()
        self.player_data = None
        self.root_save = None

        main_layout = QVBoxLayout(self)

        # 1. Identity Group
        identity_group = QGroupBox("Character Identity")
        identity_layout = QFormLayout(identity_group)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter character name...")
        
        identity_layout.addRow("Character Name:", self.name_input)
        main_layout.addWidget(identity_group)
        main_layout.addStretch()

    def load_data(self, player_data, root_save=None):
        """Loads data, looking first at the outer .fch wrapper, with fallback to inner data."""
        self.player_data = player_data
        self.root_save = root_save

        # fallback logic, first check outer container, then inner player data, no reason except fun and to show that we can.
        char_name = "Viking"
        if self.root_save and "character_name" in self.root_save:
            char_name = self.root_save["character_name"]
        elif self.player_data and "character_name" in self.player_data:
            char_name = self.player_data["character_name"]

        self.name_input.setText(char_name)

    def save_changes(self):
        """Writes changes directly to the outer container dictionary."""
        new_name = self.name_input.text().strip()
        if not new_name:
            return
        # write to outer container if available
        if self.root_save:
            self.root_save["character_name"] = new_name
            
        # now inner player data, if available
        if self.player_data:
            self.player_data["character_name"] = new_name