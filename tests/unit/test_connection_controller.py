from collections import deque

from modem_controller.transport.serial_port import SerialPortError, SerialSettings
from modem_controller.ui.connection_controller import (
    ConnectionController,
    SerialConnectionWorker,
)


class FakePort:
    def __init__(self) -> None:
        self.is_open = False
        self.settings: SerialSettings | None = None
        self.received: deque[bytes] = deque()
        self.writes: list[tuple[bytes, bool]] = []

    def open(self, settings: SerialSettings) -> None:
        self.is_open = True
        self.settings = settings

    def close(self) -> None:
        self.is_open = False

    def read_available(self) -> bytes:
        return self.received.popleft() if self.received else b""

    def write(self, payload: bytes) -> int:
        if not self.is_open:
            raise SerialPortError("port is closed")
        self.writes.append((payload, False))
        return len(payload)

    def write_sensitive(self, payload: bytes) -> int:
        if not self.is_open:
            raise SerialPortError("port is closed")
        self.writes.append((payload, True))
        return len(payload)


def test_worker_opens_sends_receives_and_closes_without_ui_thread_io(qtbot) -> None:
    port = FakePort()
    worker = SerialConnectionWorker(lambda: port)
    connected: list[str] = []
    received: list[bytes] = []
    worker.connected.connect(connected.append)
    worker.received.connect(received.append)

    worker.open(SerialSettings(port="COM10", baud_rate=19200))
    worker.send(b"AT\r", False)
    worker.send(b"AT+CPIN=1234\r", True)
    port.received.append(b"AT\r\r\nOK\r\n")
    worker.poll()
    worker.close()

    assert connected == ["COM10 | 19200 Bd | 8N1 | Kein"]
    assert port.writes == [(b"AT\r", False), (b"AT+CPIN=1234\r", True)]
    assert received == [b"AT\r\r\nOK\r\n"]
    assert not port.is_open


def test_controller_shutdown_closes_the_worker_owned_port(qtbot) -> None:
    port = FakePort()
    controller = ConnectionController(port_factory=lambda: port)

    with qtbot.waitSignal(controller.connected, timeout=1_000):
        controller.open(SerialSettings(port="COM10"))
    controller.shutdown()

    assert not port.is_open
