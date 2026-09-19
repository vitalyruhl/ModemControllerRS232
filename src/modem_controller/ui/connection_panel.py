"""Connection controls that expose user intent without touching serial hardware."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from modem_controller.transport.serial_port import FlowControl, Parity, SerialSettings


class ConnectionPanel(QWidget):
    """Presents connection state and settings; an application controller owns I/O."""

    connect_requested = Signal()
    disconnect_requested = Signal()
    refresh_requested = Signal()
    find_settings_requested = Signal()
    diagnostics_requested = Signal()
    cancel_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.port_selector = QComboBox(self)
        self.port_selector.setObjectName("portSelector")
        self.port_selector.setEditable(False)
        self.port_selector.addItem("Kein Port")

        self.status = QLabel("Getrennt", self)
        self.status.setObjectName("connectionStatus")
        self.effective_settings = QLabel("Keine Verbindung", self)

        self.connect_button = QPushButton("Verbinden", self)
        self.disconnect_button = QPushButton("Trennen", self)
        self.refresh_button = QPushButton("Aktualisieren", self)
        self.find_button = QPushButton("Einstellungen suchen", self)
        self.diagnostics_button = QPushButton("Diagnose starten", self)
        self.cancel_button = QPushButton("Stopp", self)
        self.disconnect_button.setEnabled(False)
        self.diagnostics_button.setEnabled(False)
        self.cancel_button.setEnabled(False)

        self.connect_button.clicked.connect(self.connect_requested)
        self.disconnect_button.clicked.connect(self.disconnect_requested)
        self.refresh_button.clicked.connect(self.refresh_requested)
        self.find_button.clicked.connect(self.find_settings_requested)
        self.diagnostics_button.clicked.connect(self.diagnostics_requested)
        self.cancel_button.clicked.connect(self.cancel_requested)

        self.advanced = QGroupBox("Erweiterte Verbindung", self)
        self.advanced.setCheckable(True)
        self.advanced.setChecked(False)
        advanced_layout = QFormLayout(self.advanced)
        self.baud_rate = QComboBox(self.advanced)
        self.baud_rate.addItems(["9600", "19200", "38400", "57600", "115200"])
        self.baud_rate.setCurrentText("115200")
        self.data_bits = QComboBox(self.advanced)
        self.data_bits.addItems(["8", "7"])
        self.parity = QComboBox(self.advanced)
        self.parity.addItems(["N", "E", "O"])
        self.stop_bits = QComboBox(self.advanced)
        self.stop_bits.addItems(["1", "2"])
        self.flow_control = QComboBox(self.advanced)
        self.flow_control.addItems(["Kein", "RTS/CTS", "DSR/DTR"])
        self.deadline = QSpinBox(self.advanced)
        self.deadline.setRange(100, 60_000)
        self.deadline.setValue(2_000)
        self.deadline.setSuffix(" ms")
        advanced_layout.addRow("Baudrate", self.baud_rate)
        advanced_layout.addRow("Datenbits", self.data_bits)
        advanced_layout.addRow("Parität", self.parity)
        advanced_layout.addRow("Stoppbits", self.stop_bits)
        advanced_layout.addRow("Flusssteuerung", self.flow_control)
        advanced_layout.addRow("Antwortfrist", self.deadline)

        buttons = QHBoxLayout()
        for button in (
            self.connect_button,
            self.disconnect_button,
            self.refresh_button,
            self.find_button,
            self.diagnostics_button,
            self.cancel_button,
        ):
            buttons.addWidget(button)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow("COM-Port", self.port_selector)
        form.addRow("Status", self.status)
        form.addRow("Aktiv", self.effective_settings)
        layout.addLayout(form)
        layout.addLayout(buttons)
        layout.addWidget(self.advanced)

    def set_ports(self, ports: list[str]) -> None:
        selected = self.port_selector.currentText()
        self.port_selector.clear()
        self.port_selector.addItems(ports or ["Kein Port"])
        if selected in ports:
            self.port_selector.setCurrentText(selected)

    def set_connected(self, connected: bool, settings: str = "") -> None:
        self.status.setText("Verbunden" if connected else "Getrennt")
        self.effective_settings.setText(settings or "Keine Verbindung")
        self.connect_button.setEnabled(not connected)
        self.disconnect_button.setEnabled(connected)
        self.diagnostics_button.setEnabled(connected)

    def selected_settings(self) -> SerialSettings:
        port = self.port_selector.currentText()
        if port == "Kein Port":
            raise ValueError("Bitte zuerst einen COM-Port auswählen.")
        flow_control = {
            "Kein": FlowControl.NONE,
            "RTS/CTS": FlowControl.RTS_CTS,
            "DSR/DTR": FlowControl.DSR_DTR,
        }[self.flow_control.currentText()]
        return SerialSettings(
            port=port,
            baud_rate=int(self.baud_rate.currentText()),
            data_bits=int(self.data_bits.currentText()),
            parity=Parity(self.parity.currentText()),
            stop_bits=float(self.stop_bits.currentText()),
            flow_control=flow_control,
            write_timeout=self.deadline.value() / 1_000,
        )

    def set_connecting(self) -> None:
        self.status.setText("Verbinden...")
        self.connect_button.setEnabled(False)

    def preferences(self) -> dict[str, str]:
        return {
            "port": self.port_selector.currentText(),
            "baud_rate": self.baud_rate.currentText(),
            "data_bits": self.data_bits.currentText(),
            "parity": self.parity.currentText(),
            "stop_bits": self.stop_bits.currentText(),
            "flow_control": self.flow_control.currentText(),
            "deadline_ms": str(self.deadline.value()),
        }

    def apply_preferences(self, preferences: dict[str, str]) -> None:
        port = preferences.get("port", "")
        if port and port != "Kein Port":
            if self.port_selector.findText(port) < 0:
                self.port_selector.addItem(port)
            self.port_selector.setCurrentText(port)
        for selector, key in (
            (self.baud_rate, "baud_rate"),
            (self.data_bits, "data_bits"),
            (self.parity, "parity"),
            (self.stop_bits, "stop_bits"),
            (self.flow_control, "flow_control"),
        ):
            value = preferences.get(key)
            if value is not None and selector.findText(value) >= 0:
                selector.setCurrentText(value)
        deadline = preferences.get("deadline_ms")
        if deadline is not None and deadline.isdecimal():
            self.deadline.setValue(int(deadline))

    def apply_settings(self, settings: SerialSettings) -> None:
        self.apply_preferences(
            {
                "port": settings.port,
                "baud_rate": str(settings.baud_rate),
                "data_bits": str(settings.data_bits),
                "parity": settings.parity.value,
                "stop_bits": f"{settings.stop_bits:g}",
                "flow_control": {
                    FlowControl.NONE: "Kein",
                    FlowControl.RTS_CTS: "RTS/CTS",
                    FlowControl.DSR_DTR: "DSR/DTR",
                }[settings.flow_control],
            }
        )

    def set_workflow_active(self, active: bool) -> None:
        self.cancel_button.setEnabled(active)
        self.find_button.setEnabled(not active)
        self.diagnostics_button.setEnabled(
            not active and not self.connect_button.isEnabled()
        )

    def show_error(self, message: str) -> None:
        self.status.setText(f"Fehler: {message}")
        self.connect_button.setEnabled(True)
        self.disconnect_button.setEnabled(False)
