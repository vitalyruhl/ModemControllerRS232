"""The compact desktop shell for manual terminal work."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QGroupBox,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from modem_controller.catalog.models import (
    CatalogCommand,
    CommandCatalog,
    load_starter_catalog,
)
from modem_controller.transport.serial_port import available_ports
from modem_controller.ui.connection_panel import ConnectionPanel
from modem_controller.ui.terminal_view import TerminalWorkspace


class MainWindow(QMainWindow):
    """Composes catalog selection and terminal intent without performing I/O."""

    text_send_requested = Signal(str, bytes, bool)
    bytes_send_requested = Signal(bytes)
    preset_requested = Signal(object)

    def __init__(
        self,
        catalog: CommandCatalog | None = None,
        *,
        port_provider: Callable[[], list[str]] = available_ports,
    ) -> None:
        super().__init__()
        self._catalog = catalog or load_starter_catalog()
        self._port_provider = port_provider
        self._workflow_active = False
        self._preset_execution_enabled = False
        self.setWindowTitle("Modem Controller")
        self.resize(1_080, 720)

        self.connection_panel = ConnectionPanel(self)
        self.profile_selector = QComboBox(self)
        self.profile_selector.setObjectName("profileSelector")
        self.category_selector = QComboBox(self)
        self.category_selector.setObjectName("categorySelector")
        self.notes = QPlainTextEdit(self)
        self.notes.setReadOnly(True)
        self.notes.setMaximumBlockCount(20)
        self.notes.setObjectName("profileNotes")
        self.command_group = QGroupBox("Befehle", self)
        self.command_layout = QGridLayout(self.command_group)
        self.terminal = TerminalWorkspace(parent=self)

        for profile in self._catalog.profiles:
            self.profile_selector.addItem(profile.name, profile.id)
        self.profile_selector.currentIndexChanged.connect(self._change_profile)
        self.category_selector.currentTextChanged.connect(self._render_commands)
        self.connection_panel.refresh_requested.connect(self.refresh_ports)
        self.terminal.text_submitted.connect(self.text_send_requested)
        self.terminal.bytes_submitted.connect(self.bytes_send_requested)

        sidebar = QWidget(self)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.addWidget(self.connection_panel)
        sidebar_layout.addWidget(self.profile_selector)
        sidebar_layout.addWidget(self.category_selector)
        sidebar_layout.addWidget(self.notes)
        sidebar_layout.addWidget(self.command_group)
        sidebar_layout.addStretch(1)

        splitter = QSplitter(self)
        splitter.addWidget(sidebar)
        splitter.addWidget(self.terminal)
        splitter.setSizes([330, 750])
        self.setCentralWidget(splitter)
        self._change_profile()
        self.refresh_ports()

    def refresh_ports(self) -> None:
        """Refresh port choices without opening or connecting to a serial port."""

        try:
            self.connection_panel.set_ports(self._port_provider())
        except OSError as error:
            self.connection_panel.show_error(str(error))

    def set_workflow_active(self, active: bool) -> None:
        self._workflow_active = active
        self.terminal.set_workflow_active(active)
        self.connection_panel.set_workflow_active(active)
        self._render_commands()

    def set_preset_execution_enabled(self, enabled: bool) -> None:
        self._preset_execution_enabled = enabled
        self._render_commands()

    def _change_profile(self) -> None:
        profile = self._selected_profile()
        self.notes.setPlainText(
            profile.shipped_notes + self._user_notes(profile.user_notes)
        )
        current = self.category_selector.currentText()
        categories = sorted({command.category for command in profile.visible_commands})
        self.category_selector.blockSignals(True)
        self.category_selector.clear()
        self.category_selector.addItems(categories)
        if current in categories:
            self.category_selector.setCurrentText(current)
        self.category_selector.blockSignals(False)
        self._render_commands()

    def _render_commands(self) -> None:
        while self.command_layout.count():
            item = self.command_layout.takeAt(0)
            if item.widget() is not None:
                item.widget().deleteLater()

        category = self.category_selector.currentText()
        commands = [
            command
            for command in self._selected_profile().visible_commands
            if command.category == category
        ]
        for index, command in enumerate(commands):
            button = QPushButton(command.label, self.command_group)
            button.setToolTip(command.help_text)
            button.setEnabled(
                self._preset_execution_enabled and not self._workflow_active
            )
            button.clicked.connect(
                lambda checked=False, selected=command: self._request_preset(selected)
            )
            self.command_layout.addWidget(button, index // 2, index % 2)

    def _request_preset(self, command: CatalogCommand) -> None:
        if self._preset_execution_enabled and not self._workflow_active:
            self.preset_requested.emit(command)

    def _selected_profile(self):
        return self._catalog.profile(self.profile_selector.currentData())

    @staticmethod
    def _user_notes(notes: str) -> str:
        return f"\n\n{notes}" if notes else ""
