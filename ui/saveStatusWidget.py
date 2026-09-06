from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from subscripts.saveHealth import (
    SAVE_STATE_COMPATIBILITY_UNVERIFIED,
    SAVE_STATE_NEEDS_ATTENTION,
    SAVE_STATE_VERIFIED,
    SaveHealthReport,
)


class SaveStatusWidget(QFrame):
    """Compact player-facing summary of verification and compatibility state."""

    _STATE_COLORS = {
        SAVE_STATE_VERIFIED: "#8ad7c1",
        SAVE_STATE_COMPATIBILITY_UNVERIFIED: "#f0c878",
        SAVE_STATE_NEEDS_ATTENTION: "#ee9b96",
    }

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("saveStatus")
        self.setAccessibleName("Character save status")
        self.setStyleSheet(
            "QFrame#saveStatus { background-color: #0b1c24; border: 1px solid #284451; "
            "border-radius: 7px; }"
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(3)

        self.state_label = QLabel()
        self.state_label.setObjectName("saveStatusState")
        self.meta_label = QLabel()
        self.meta_label.setWordWrap(True)
        self.meta_label.setStyleSheet("color: #c4d8df;")
        self.detail_label = QLabel()
        self.detail_label.setWordWrap(True)
        self.detail_label.setStyleSheet("color: #a9c1ca;")

        layout.addWidget(self.state_label)
        layout.addWidget(self.meta_label)
        layout.addWidget(self.detail_label)
        self.clear()

    def clear(self):
        self.state_label.setText("No character loaded")
        self.state_label.setStyleSheet("font-weight: 700; color: #d7e8ee;")
        self.meta_label.setText("")
        self.detail_label.setText(
            "Open a character to see verification, save version, source, and compatibility status."
        )
        self.setAccessibleDescription(self.detail_label.text())

    def set_report(self, report: SaveHealthReport):
        self.state_label.setText(report.state)
        color = self._STATE_COLORS.get(report.state, "#d7e8ee")
        self.state_label.setStyleSheet(f"font-weight: 700; color: {color};")

        meta = [
            f"Save {report.save_version_label}",
            report.source,
            f"Modified: {report.modified_label}",
            f"Catalog: {report.catalog_label}",
        ]
        if report.backup_label:
            meta.append(f"Backup: {report.backup_label}")
        self.meta_label.setText("  •  ".join(meta))
        self.detail_label.setText(report.detail)
        self.setAccessibleDescription(f"{report.state}. {report.detail}")
