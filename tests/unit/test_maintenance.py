from modem_controller.catalog.models import load_starter_catalog
from modem_controller.protocol.at_session import AtExchange, ExchangeOutcome
from modem_controller.workflows.maintenance import (
    MaintenanceOutcome,
    MaintenanceRunner,
)
from modem_controller.workflows.reporting import redact


def exchange(
    command: bytes,
    *,
    outcome: ExchangeOutcome = ExchangeOutcome.COMPLETED,
    final: bytes | None = b"OK",
) -> AtExchange:
    return AtExchange(command, 0, 1, (), (), (), (), False, outcome, final)


def test_cancelled_maintenance_action_emits_no_bytes() -> None:
    command = load_starter_catalog().profile("generic-at").command("restart-modem")
    sent: list[bytes] = []
    result = MaintenanceRunner(
        lambda payload: sent.append(payload) or exchange(payload)
    ).run(command, {}, confirmed=False)

    assert result.outcome is MaintenanceOutcome.CANCELLED
    assert not result.session_invalidated
    assert sent == []


def test_pin_is_transient_and_marks_a_capture_gap() -> None:
    command = load_starter_catalog().profile("generic-at").command("unlock-sim")
    sent: list[bytes] = []
    result = MaintenanceRunner(
        lambda payload: sent.append(payload) or exchange(payload)
    ).run(command, {"pin": "1234"}, confirmed=True)

    assert sent == [b"AT+CPIN=1234\r"]
    assert result.outcome is MaintenanceOutcome.COMPLETED
    assert result.evidence == (b"OK",)
    assert result.capture_gap is not None
    assert "1234" not in str(result)
    assert redact("AT+CPIN=1234") == "<sensitive input redacted>"


def test_timeout_is_inconclusive_and_is_not_retried() -> None:
    command = load_starter_catalog().profile("generic-at").command("restore-defaults")
    sent: list[bytes] = []
    result = MaintenanceRunner(
        lambda payload: sent.append(payload)
        or exchange(payload, outcome=ExchangeOutcome.TIMED_OUT, final=None)
    ).run(command, {}, confirmed=True)

    assert sent == [b"AT&F\r"]
    assert result.outcome is MaintenanceOutcome.INCONCLUSIVE
    assert result.session_invalidated
    assert "Do not retry" in result.next_action
