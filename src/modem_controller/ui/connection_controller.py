"""Thread-owned serial connection lifecycle for the Qt desktop shell."""

from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from threading import Event
from time import monotonic

from PySide6.QtCore import QMetaObject, QObject, Qt, QThread, QTimer, Signal, Slot

from modem_controller.catalog.models import CatalogCommand, DeviceProfile
from modem_controller.protocol.at_session import (
    AtExchange,
    AtSession,
    AtSessionError,
    ExchangeOutcome,
)
from modem_controller.transport.serial_port import (
    FlowControl,
    SerialPort,
    SerialPortError,
    SerialSettings,
)
from modem_controller.workflows.connection_search import (
    ConnectionSearchResult,
    ConnectionSearchRunner,
)
from modem_controller.workflows.diagnostics import DiagnosticRunner
from modem_controller.workflows.maintenance import MaintenanceRunner
from modem_controller.workflows.sms import SmsInspector, SmsMessage, SmsSendWorkflow

PortFactory = Callable[[], SerialPort]


class SerialConnectionWorker(QObject):
    """Owns serial I/O in its worker thread and emits UI-safe events."""

    connected = Signal(str)
    disconnected = Signal()
    received = Signal(bytes)
    control_bytes_sent = Signal(bytes)
    error = Signal(str)
    diagnostics_completed = Signal(object)
    search_completed = Signal(object)
    maintenance_completed = Signal(object)
    sms_completed = Signal(object)
    sms_status_completed = Signal(object)
    workflow_finished = Signal()

    def __init__(
        self,
        port_factory: PortFactory = SerialPort,
        *,
        cancel_requested: Event | None = None,
    ) -> None:
        super().__init__()
        self._port_factory = port_factory
        self._port: SerialPort | None = None
        self._poll_timer: QTimer | None = None
        self._cancel_requested = cancel_requested or Event()

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
        self._write(payload, sensitive=sensitive)

    @Slot(bytes)
    def send_control_bytes(self, payload: bytes) -> None:
        if self._write(payload, sensitive=False):
            self.control_bytes_sent.emit(payload)

    def _write(self, payload: bytes, *, sensitive: bool) -> bool:
        port = self._port
        if port is None or not port.is_open:
            self.error.emit("No serial connection is open.")
            return False
        try:
            if sensitive:
                port.write_sensitive(payload)
            else:
                port.write(payload)
        except SerialPortError as error:
            self.error.emit(str(error))
            self.close()
            return False
        return True

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

    @Slot(object)
    def run_diagnostics(self, profile: DeviceProfile) -> None:
        port = self._port
        if port is None or not port.is_open:
            self.error.emit("No serial connection is open.")
            self.workflow_finished.emit()
            return
        self._cancel_requested.clear()
        session = AtSession(port, clock=monotonic)
        try:
            results = DiagnosticRunner(
                lambda command: self._exchange(
                    session,
                    command.render() + b"\r",
                    timeout=command.timeout_seconds,
                ),
                cancelled=self._cancel_requested.is_set,
            ).run(profile)
        finally:
            self.diagnostics_completed.emit(locals().get("results", ()))
            self.workflow_finished.emit()

    @Slot(str)
    def search_settings(self, port_name: str) -> None:
        if self._port is not None and self._port.is_open:
            self.error.emit(
                "Settings can only be searched while no connection is open."
            )
            self.workflow_finished.emit()
            return
        self._cancel_requested.clear()
        try:
            result = ConnectionSearchRunner(
                self._probe_settings, cancelled=self._cancel_requested.is_set
            ).run(ConnectionSearchRunner.quick_candidates(port_name))
        finally:
            self.search_completed.emit(locals().get("result", _empty_search_result()))
            self.workflow_finished.emit()

    @Slot(object, object)
    def run_maintenance(self, command: CatalogCommand, values: dict[str, str]) -> None:
        port = self._port
        if port is None or not port.is_open:
            self.error.emit("No serial connection is open.")
            self.workflow_finished.emit()
            return
        try:
            result = MaintenanceRunner(
                lambda payload: self._exchange(
                    AtSession(port, clock=monotonic),
                    payload,
                    timeout=command.timeout_seconds,
                )
            ).run(command, values, confirmed=True)
        except ValueError as error:
            self.error.emit(str(error))
            result = None
        self.maintenance_completed.emit(result)
        self.close()
        self.workflow_finished.emit()

    @Slot(str, str)
    def send_sms(self, recipient: str, body: str) -> None:
        port = self._port
        if port is None or not port.is_open:
            self.error.emit("No serial connection is open.")
            self.workflow_finished.emit()
            return
        try:
            workflow = SmsSendWorkflow(
                AtSession(port, clock=monotonic),
                completion_timeout=timedelta(seconds=60),
            )
            workflow.begin(SmsMessage(recipient, body), confirmed=True)
            while True:
                if self._cancel_requested.is_set():
                    result = workflow.cancel()
                    break
                result = workflow.poll()
                if result is not None:
                    break
                QThread.msleep(10)
        except ValueError as error:
            self.error.emit(str(error))
            result = None
        self.sms_completed.emit(result)
        self.workflow_finished.emit()

    @Slot(int)
    def read_sms(self, index: int) -> None:
        self._run_sms_queries((SmsInspector.read_message(index, confirmed=True),))

    @Slot()
    def query_sms_status(self) -> None:
        self._run_sms_queries(SmsInspector.status_commands())

    def _run_sms_queries(self, payloads: tuple[bytes, ...]) -> None:
        port = self._port
        if port is None or not port.is_open:
            self.error.emit("No serial connection is open.")
            self.workflow_finished.emit()
            return
        try:
            session = AtSession(port, clock=monotonic)
            exchanges = tuple(
                self._exchange(session, payload, timeout=10) for payload in payloads
            )
        finally:
            self.sms_status_completed.emit(locals().get("exchanges", ()))
            self.workflow_finished.emit()

    def _ensure_poll_timer(self) -> QTimer:
        if self._poll_timer is None:
            self._poll_timer = QTimer(self)
            self._poll_timer.timeout.connect(self.poll)
        return self._poll_timer

    def _exchange(
        self, session: AtSession, payload: bytes, *, timeout: float
    ) -> AtExchange:
        started_at = monotonic()
        try:
            session.start(payload, timeout=timedelta(seconds=timeout))
            while True:
                if self._cancel_requested.is_set():
                    return session.cancel()
                completed = session.poll()
                if completed is not None:
                    return completed
                QThread.msleep(10)
        except AtSessionError as error:
            self.error.emit(str(error))
            return AtExchange(
                payload,
                started_at,
                monotonic(),
                (),
                (),
                (),
                (),
                False,
                ExchangeOutcome.DISCONNECTED,
            )

    def _probe_settings(self, settings: SerialSettings, payload: bytes) -> AtExchange:
        port = self._port_factory()
        started_at = monotonic()
        try:
            port.open(settings)
            return self._exchange(AtSession(port, clock=monotonic), payload, timeout=2)
        except SerialPortError:
            return AtExchange(
                payload,
                started_at,
                monotonic(),
                (),
                (),
                (),
                (),
                False,
                ExchangeOutcome.DISCONNECTED,
            )
        finally:
            port.close()


class ConnectionController(QObject):
    """Forwards UI intents to a thread-owned serial worker without auto-connecting."""

    connected = Signal(str)
    disconnected = Signal()
    received = Signal(bytes)
    control_bytes_sent = Signal(bytes)
    error = Signal(str)
    diagnostics_completed = Signal(object)
    search_completed = Signal(object)
    maintenance_completed = Signal(object)
    sms_completed = Signal(object)
    sms_status_completed = Signal(object)
    workflow_finished = Signal()

    _open_requested = Signal(object)
    _close_requested = Signal()
    _send_requested = Signal(bytes, bool)
    _control_bytes_requested = Signal(bytes)
    _diagnostics_requested = Signal(object)
    _search_requested = Signal(str)
    _maintenance_requested = Signal(object, object)
    _sms_requested = Signal(str, str)
    _sms_read_requested = Signal(int)
    _sms_status_requested = Signal()

    def __init__(
        self,
        *,
        port_factory: PortFactory = SerialPort,
        parent: QObject | None = None,
    ) -> None:
        super().__init__(parent)
        self._cancel_requested = Event()
        self._thread = QThread(self)
        self._worker = SerialConnectionWorker(
            port_factory, cancel_requested=self._cancel_requested
        )
        self._worker.moveToThread(self._thread)
        self._thread.finished.connect(self._worker.deleteLater)
        self._open_requested.connect(self._worker.open, Qt.QueuedConnection)
        self._close_requested.connect(self._worker.close, Qt.QueuedConnection)
        self._send_requested.connect(self._worker.send, Qt.QueuedConnection)
        self._control_bytes_requested.connect(
            self._worker.send_control_bytes, Qt.QueuedConnection
        )
        self._diagnostics_requested.connect(
            self._worker.run_diagnostics, Qt.QueuedConnection
        )
        self._search_requested.connect(
            self._worker.search_settings, Qt.QueuedConnection
        )
        self._maintenance_requested.connect(
            self._worker.run_maintenance, Qt.QueuedConnection
        )
        self._sms_requested.connect(self._worker.send_sms, Qt.QueuedConnection)
        self._sms_read_requested.connect(self._worker.read_sms, Qt.QueuedConnection)
        self._sms_status_requested.connect(
            self._worker.query_sms_status, Qt.QueuedConnection
        )
        self._worker.connected.connect(self._relay_connected)
        self._worker.disconnected.connect(self._relay_disconnected)
        self._worker.received.connect(self._relay_received)
        self._worker.control_bytes_sent.connect(self.control_bytes_sent)
        self._worker.error.connect(self._relay_error)
        self._worker.diagnostics_completed.connect(self.diagnostics_completed)
        self._worker.search_completed.connect(self.search_completed)
        self._worker.maintenance_completed.connect(self.maintenance_completed)
        self._worker.sms_completed.connect(self.sms_completed)
        self._worker.sms_status_completed.connect(self.sms_status_completed)
        self._worker.workflow_finished.connect(self.workflow_finished)
        self._thread.start()

    def open(self, settings: SerialSettings) -> None:
        self._open_requested.emit(settings)

    def close(self) -> None:
        self._close_requested.emit()

    def send(self, payload: bytes, *, sensitive: bool = False) -> None:
        self._send_requested.emit(payload, sensitive)

    def send_control_bytes(self, payload: bytes) -> None:
        self._control_bytes_requested.emit(payload)

    def run_diagnostics(self, profile: DeviceProfile) -> None:
        self._cancel_requested.clear()
        self._diagnostics_requested.emit(profile)

    def cancel_workflow(self) -> None:
        self._cancel_requested.set()

    def search_settings(self, port_name: str) -> None:
        self._cancel_requested.clear()
        self._search_requested.emit(port_name)

    def run_maintenance(self, command: CatalogCommand, values: dict[str, str]) -> None:
        self._maintenance_requested.emit(command, values)

    def send_sms(self, recipient: str, body: str) -> None:
        self._cancel_requested.clear()
        self._sms_requested.emit(recipient, body)

    def read_sms(self, index: int) -> None:
        self._cancel_requested.clear()
        self._sms_read_requested.emit(index)

    def query_sms_status(self) -> None:
        self._cancel_requested.clear()
        self._sms_status_requested.emit()

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


def _empty_search_result() -> ConnectionSearchResult:
    return ConnectionSearchResult((), None)
