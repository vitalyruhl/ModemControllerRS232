"""Shared terminal transcript and command input widgets."""

from __future__ import annotations

import re
from collections import deque
from dataclasses import dataclass
from enum import Enum

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class DisplayMode(str, Enum):
    TEXT = "Text"
    HEX = "Hex"
    COMBINED = "Text + Hex"


class TerminalDirection(str, Enum):
    RECEIVED = "RX"
    TRANSMITTED = "TX"


@dataclass(frozen=True, slots=True)
class TerminalEntry:
    direction: TerminalDirection
    data: bytes
    sensitive: bool = False


_SENSITIVE_COMMAND = re.compile(r"^AT\+(?:CPIN|CLCK|CPWD)\b", re.IGNORECASE)
_TERMINATORS = {"None": b"", "CR": b"\r", "LF": b"\n", "CRLF": b"\r\n"}


class TerminalWorkspace(QWidget):
    """A bounded transcript and one explicit text or exact-byte send intent."""

    text_submitted = Signal(str, bytes, bool)
    bytes_submitted = Signal(bytes)

    def __init__(
        self, *, max_entries: int = 1_000, parent: QWidget | None = None
    ) -> None:
        super().__init__(parent)
        if max_entries <= 0:
            raise ValueError("max_entries must be positive")

        self._entries: deque[TerminalEntry] = deque(maxlen=max_entries)
        self._auto_scroll = True
        self._workflow_active = False

        self.transcript = QPlainTextEdit(self)
        self.transcript.setReadOnly(True)
        self.transcript.setObjectName("terminalTranscript")
        self.transcript.verticalScrollBar().valueChanged.connect(self._track_scroll)

        self.display_mode = QComboBox(self)
        self.display_mode.addItems([mode.value for mode in DisplayMode])
        self.display_mode.currentTextChanged.connect(lambda _: self._render())

        self.command_input = QLineEdit(self)
        self.command_input.setObjectName("terminalInput")
        self.command_input.setPlaceholderText("AT command")
        self.command_input.returnPressed.connect(self.submit_text)

        self.terminator = QComboBox(self)
        self.terminator.addItems(_TERMINATORS)
        self.terminator.setCurrentText("CR")

        self.send_button = QPushButton("Senden", self)
        self.send_button.clicked.connect(self.submit_text)

        self.hex_input = QLineEdit(self)
        self.hex_input.setObjectName("hexInput")
        self.hex_input.setPlaceholderText("41 54 0D")
        self.hex_input.returnPressed.connect(self.submit_hex)
        self.hex_send_button = QPushButton("Hex senden", self)
        self.hex_send_button.clicked.connect(self.submit_hex)
        self.validation_message = QLabel(self)
        self.validation_message.setObjectName("terminalValidation")

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.command_input, 1)
        input_layout.addWidget(self.terminator)
        input_layout.addWidget(self.send_button)

        hex_layout = QHBoxLayout()
        hex_layout.addWidget(self.hex_input, 1)
        hex_layout.addWidget(self.hex_send_button)

        controls = QFormLayout()
        controls.addRow("Anzeige", self.display_mode)
        controls.addRow("Befehl", input_layout)
        controls.addRow("Exakte Bytes", hex_layout)
        controls.addRow("", self.validation_message)

        layout = QVBoxLayout(self)
        layout.addWidget(self.transcript, 1)
        layout.addLayout(controls)

    @property
    def entries(self) -> tuple[TerminalEntry, ...]:
        return tuple(self._entries)

    @property
    def is_auto_scroll_paused(self) -> bool:
        return not self._auto_scroll

    def set_workflow_active(self, active: bool) -> None:
        self._workflow_active = active
        self.command_input.setEnabled(not active)
        self.send_button.setEnabled(not active)
        self.hex_input.setEnabled(not active)
        self.hex_send_button.setEnabled(not active)

    def set_auto_scroll_paused(self, paused: bool) -> None:
        self._auto_scroll = not paused

    def append_received(self, data: bytes) -> None:
        self._append(TerminalDirection.RECEIVED, data)

    def append_transmitted(self, data: bytes, *, sensitive: bool = False) -> None:
        self._append(TerminalDirection.TRANSMITTED, data, sensitive=sensitive)

    def clear(self) -> None:
        self._entries.clear()
        self.transcript.clear()

    def submit_text(self) -> bool:
        if self._workflow_active:
            self.validation_message.setText("Aktiver Ablauf belegt die Sitzung.")
            return False
        command = self.command_input.text()
        if not command:
            return False
        terminator = _TERMINATORS[self.terminator.currentText()]
        sensitive = bool(_SENSITIVE_COMMAND.match(command))
        self.append_transmitted(
            command.encode("ascii", errors="replace") + terminator, sensitive=sensitive
        )
        self.text_submitted.emit(command, terminator, sensitive)
        if not sensitive:
            self.command_input.clear()
        self.validation_message.clear()
        return True

    def submit_hex(self) -> bool:
        if self._workflow_active:
            self.validation_message.setText("Aktiver Ablauf belegt die Sitzung.")
            return False
        try:
            payload = self._parse_hex(self.hex_input.text())
        except ValueError as error:
            self.validation_message.setText(str(error))
            return False
        self.append_transmitted(payload)
        self.bytes_submitted.emit(payload)
        self.hex_input.clear()
        self.validation_message.clear()
        return True

    @staticmethod
    def _parse_hex(value: str) -> bytes:
        compact = "".join(value.split())
        if not compact:
            raise ValueError("Hex-Eingabe fehlt.")
        if len(compact) % 2 or re.fullmatch(r"[0-9A-Fa-f]+", compact) is None:
            raise ValueError("Ungültige Hex-Eingabe.")
        return bytes.fromhex(compact)

    def _append(
        self, direction: TerminalDirection, data: bytes, *, sensitive: bool = False
    ) -> None:
        self._entries.append(
            TerminalEntry(direction=direction, data=bytes(data), sensitive=sensitive)
        )
        self._render()

    def _render(self) -> None:
        lines = [self._format_entry(entry) for entry in self._entries]
        self.transcript.setPlainText("\n".join(lines))
        if self._auto_scroll:
            scroll_bar = self.transcript.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum())

    def _format_entry(self, entry: TerminalEntry) -> str:
        if entry.sensitive and entry.direction is TerminalDirection.TRANSMITTED:
            return "TX  <sensitive command suppressed>"
        mode = DisplayMode(self.display_mode.currentText())
        text = entry.data.decode("utf-8", errors="replace")
        hexadecimal = entry.data.hex(" ").upper()
        if mode is DisplayMode.TEXT:
            payload = text
        elif mode is DisplayMode.HEX:
            payload = hexadecimal
        else:
            payload = f"{text}  [{hexadecimal}]"
        return f"{entry.direction.value}  {payload}"

    def _track_scroll(self, value: int) -> None:
        scroll_bar = self.transcript.verticalScrollBar()
        self._auto_scroll = value >= scroll_bar.maximum()
