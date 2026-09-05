import sys

from PySide6.QtWidgets import QApplication

from ui.mainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    if "--smoke-test" in sys.argv:
        window.show()
        app.processEvents()
        window.close()
        return 0

    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
