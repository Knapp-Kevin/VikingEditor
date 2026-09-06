import sys

from PySide6.QtWidgets import QApplication

from ui.branding import app_icon
from ui.mainWindow import MainWindow


def _verify_catalog_bundle() -> bool:
    from data.items import CATALOG_GAME_VERSION, CATALOG_SELECTABLE_ITEM_COUNT

    return bool(CATALOG_GAME_VERSION) and CATALOG_SELECTABLE_ITEM_COUNT >= 900


def _verify_brand_bundle() -> bool:
    from ui.branding import banner_is_usable

    return banner_is_usable()


def main():
    app = QApplication(sys.argv)
    app.setWindowIcon(app_icon())
    window = MainWindow()

    if "--smoke-test" in sys.argv:
        if not (_verify_catalog_bundle() and _verify_brand_bundle()):
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
