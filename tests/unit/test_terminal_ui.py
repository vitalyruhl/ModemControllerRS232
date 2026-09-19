from PySide6.QtCore import Qt

from modem_controller.ui.main_window import MainWindow
from modem_controller.ui.terminal_view import TerminalDirection, TerminalWorkspace


def test_startup_and_profile_selection_do_not_emit_send_intents(qtbot) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    text_intents: list[tuple[str, bytes, bool]] = []
    byte_intents: list[bytes] = []
    window.text_send_requested.connect(lambda *intent: text_intents.append(intent))
    window.bytes_send_requested.connect(byte_intents.append)

    window.profile_selector.setCurrentIndex(0)
    window.category_selector.setCurrentIndex(0)

    assert text_intents == []
    assert byte_intents == []


def test_terminal_has_read_only_transcript_and_one_enter_emits_one_terminated_intent(
    qtbot,
) -> None:
    terminal = TerminalWorkspace()
    qtbot.addWidget(terminal)
    intents: list[tuple[str, bytes, bool]] = []
    terminal.text_submitted.connect(lambda *intent: intents.append(intent))
    terminal.command_input.setText("AT")

    qtbot.keyClick(terminal.command_input, Qt.Key_Return)

    assert terminal.transcript.isReadOnly()
    assert terminal.command_input.isEnabled()
    assert intents == [("AT", b"\r", False)]
    assert terminal.entries[-1].direction is TerminalDirection.TRANSMITTED


def test_malformed_hex_is_rejected_without_a_send_intent(qtbot) -> None:
    terminal = TerminalWorkspace()
    qtbot.addWidget(terminal)
    intents: list[bytes] = []
    terminal.bytes_submitted.connect(intents.append)
    terminal.hex_input.setText("4G")

    assert not terminal.submit_hex()
    assert intents == []
    assert "Ungültig" in terminal.validation_message.text()


def test_terminal_bounds_history_and_pauses_autoscroll(qtbot) -> None:
    terminal = TerminalWorkspace(max_entries=2)
    qtbot.addWidget(terminal)
    terminal.set_auto_scroll_paused(True)
    terminal.append_received(b"first")
    terminal.append_received(b"second")
    terminal.append_received(b"third")

    assert [entry.data for entry in terminal.entries] == [b"second", b"third"]
    assert terminal.is_auto_scroll_paused


def test_active_workflow_prevents_manual_interleaving_and_port_errors_are_visible(
    qtbot,
) -> None:
    window = MainWindow()
    qtbot.addWidget(window)
    intents: list[tuple[str, bytes, bool]] = []
    window.text_send_requested.connect(lambda *intent: intents.append(intent))
    window.set_workflow_active(True)
    window.terminal.command_input.setText("AT")

    assert not window.terminal.submit_text()
    window.connection_panel.show_error("COM7 belegt")

    assert intents == []
    assert "COM7 belegt" in window.connection_panel.status.text()
