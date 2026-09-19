"""Application entry points for the desktop modem terminal."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from modem_controller.ui.main_window import MainWindow


def create_main_window() -> MainWindow:
    """Create the UI without opening a port or sending any bytes."""

    return MainWindow()


def main() -> int:
    app = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
