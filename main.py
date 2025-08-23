import sys
from PySide6.QtWidgets import QApplication
from src.gui.main_window import PrivGuardUI


def main():
    """Starte die PrivGuard App."""
    app = QApplication(sys.argv)

    window = PrivGuardUI()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()