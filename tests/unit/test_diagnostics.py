from modem_controller.catalog.models import load_starter_catalog
from modem_controller.protocol.at_session import AtExchange, ExchangeOutcome
from modem_controller.workflows.diagnostics import DiagnosticRunner, DiagnosticState


def exchange(*lines: bytes, final: bytes = b"OK") -> AtExchange:
    return AtExchange(
        b"", 0, 1, (), tuple(lines), (), (), False, ExchangeOutcome.COMPLETED, final
    )


def test_diagnostics_execute_only_allowlisted_commands_and_skip_after_sim_pin() -> None:
    profile = load_starter_catalog().profile("generic-at")
    sent: list[str] = []

    def execute(command):
        sent.append(command.id)
        return exchange(b"+CPIN: SIM PIN") if command.id == "sim-status" else exchange()

    results = DiagnosticRunner(execute).run(profile)

    assert sent == [
        "attention",
        "identity",
        "sim-status",
        "registration-status",
        "signal-quality",
        "serial-baud-rate",
    ]
    assert "unlock-sim" not in sent
    assert (
        next(result for result in results if result.command_id == "sim-status").state
        is DiagnosticState.ATTENTION
    )
    assert (
        next(result for result in results if result.command_id == "operator").state
        is DiagnosticState.SKIPPED
    )


def test_diagnostics_preserve_unknown_and_error_evidence_without_repair() -> None:
    profile = load_starter_catalog().profile("generic-at")
    runner = DiagnosticRunner(
        lambda command: exchange(b"+CSQ: 99,99")
        if command.id == "signal-quality"
        else exchange(final=b"+CME ERROR: 13")
    )

    results = runner.run(profile)

    assert (
        next(
            result for result in results if result.command_id == "signal-quality"
        ).state
        is DiagnosticState.ATTENTION
    )
    assert (
        next(result for result in results if result.command_id == "attention").state
        is DiagnosticState.UNSUPPORTED
    )
