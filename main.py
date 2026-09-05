import sys

from PySide6.QtWidgets import QApplication

from ui.mainWindow import MainWindow


def _verify_catalog_bundle() -> bool:
    from data.items import CATALOG_GAME_VERSION, CATALOG_SELECTABLE_ITEM_COUNT

    return CATALOG_GAME_VERSION == "0.221.12" and CATALOG_SELECTABLE_ITEM_COUNT >= 900


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    if "--smoke-test" in sys.argv:
        if not _verify_catalog_bundle():
            window.close()
            return 2
        window.show()
        app.processEvents()
        window.close()
        return 0

    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
