"""Thread-owned serial connection lifecycle for the Qt desktop shell."""

from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import QMetaObject, QObject, Qt, QThread, QTimer, Signal, Slot

from modem_controller.transport.serial_port import (
    FlowControl,
    SerialPort,
    SerialPortError,
    SerialSettings,
)

PortFactory = Callable[[], SerialPort]


class SerialConnectionWorker(QObject):
    """Owns serial I/O in its worker thread and emits UI-safe events."""

    connected = Signal(str)
    disconnected = Signal()
    received = Signal(bytes)
    error = Signal(str)

    def __init__(self, port_factory: PortFactory = SerialPort) -> None:
        super().__init__()
        self._port_factory = port_factory
        self._port: SerialPort | None = None
        self._poll_timer: QTimer | None = None

    @Slot(object)
    def open(self, settings: SerialSettings) -> None:
        self.close()
        port = self._port_factory()
        try:
            port.open(settings)
        except SerialPortError as error:
            self.error.emit(str(error))
            return
        self._port = port
        self._ensure_poll_timer().start(25)
        self.connected.emit(_format_settings(settings))

    @Slot()
    def close(self) -> None:
        timer = self._poll_timer
        if timer is not None:
            timer.stop()
        port = self._port
        self._port = None
        if port is not None:
            port.close()
            self.disconnected.emit()

    @Slot(bytes, bool)
    def send(self, payload: bytes, sensitive: bool) -> None:
        port = self._port
        if port is None or not port.is_open:
            self.error.emit("Keine serielle Verbindung ist geöffnet.")
            return
        try:
            if sensitive:
                port.write_sensitive(payload)
            else:
                port.write(payload)
        except SerialPortError as error:
            self.error.emit(str(error))
            self.close()

    @Slot()
    def poll(self) -> None:
        port = self._port
        if port is None or not port.is_open:
            return
        try:
            data = port.read_available()
        except SerialPortError as error:
            self.error.emit(str(error))
            self.close()
            return
        if data:
            self.received.emit(data)

    def _ensure_poll_timer(self) -> QTimer:
        if self._poll_timer is None:
            self._poll_timer = QTimer(self)
            self._poll_timer.timeout.connect(self.poll)
        return self._poll_timer


class ConnectionController(QObject):
    """Forwards UI intents to a thread-owned serial worker without auto-connecting."""

    connected = Signal(str)
    disconnected = Signal()
    received = Signal(bytes)
    error = Signal(str)

    _open_requested = Signal(object)
    _close_requested = Signal()
    _send_requested = Signal(bytes, bool)

    def __init__(
        self,
        *,
        port_factory: PortFactory = SerialPort,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._thread = QThread(self)
        self._worker = SerialConnectionWorker(port_factory)
        self._worker.moveToThread(self._thread)
        self._thread.finished.connect(self._worker.deleteLater)
        self._open_requested.connect(self._worker.open, Qt.QueuedConnection)
        self._close_requested.connect(self._worker.close, Qt.QueuedConnection)
        self._send_requested.connect(self._worker.send, Qt.QueuedConnection)
        self._worker.connected.connect(self._relay_connected)
        self._worker.disconnected.connect(self._relay_disconnected)
        self._worker.received.connect(self._relay_received)
        self._worker.error.connect(self._relay_error)
        self._thread.start()

    def open(self, settings: SerialSettings) -> None:
        self._open_requested.emit(settings)

    def close(self) -> None:
        self._close_requested.emit()

    def send(self, payload: bytes, *, sensitive: bool = False) -> None:
        self._send_requested.emit(payload, sensitive)

    def shutdown(self) -> None:
        if not self._thread.isRunning():
            return
        QMetaObject.invokeMethod(self._worker, "close", Qt.BlockingQueuedConnection)
        self._thread.quit()
        self._thread.wait(2_000)

    @Slot(str)
    def _relay_connected(self, settings: str) -> None:
        self.connected.emit(settings)

    @Slot()
    def _relay_disconnected(self) -> None:
        self.disconnected.emit()

    @Slot(bytes)
    def _relay_received(self, data: bytes) -> None:
        self.received.emit(data)

    @Slot(str)
    def _relay_error(self, message: str) -> None:
        self.error.emit(message)


def _format_settings(settings: SerialSettings) -> str:
    flow_control = {
        FlowControl.NONE: "Kein",
        FlowControl.RTS_CTS: "RTS/CTS",
        FlowControl.DSR_DTR: "DSR/DTR",
    }[settings.flow_control]
    return (
        f"{settings.port} | {settings.baud_rate} Bd | "
        f"{settings.data_bits}{settings.parity.value}{settings.stop_bits:g} | "
        f"{flow_control}"
    )
