"""Evidence-based, read-only diagnostic policy for AT command catalogs."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from modem_controller.catalog.models import CatalogCommand, DeviceProfile
from modem_controller.protocol.at_session import AtExchange, ExchangeOutcome


class DiagnosticState(str, Enum):
    OK = "ok"
    ATTENTION = "attention"
    UNKNOWN = "unknown"
    UNSUPPORTED = "unsupported"
    SKIPPED = "skipped"


@dataclass(frozen=True, slots=True)
class DiagnosticResult:
    command_id: str
    state: DiagnosticState
    evidence: tuple[bytes, ...]
    next_check: str


Execute = Callable[[CatalogCommand], AtExchange]
Cancelled = Callable[[], bool]


class DiagnosticRunner:
    """Runs only catalog-approved queries and records inconclusive evidence honestly."""

    def __init__(
        self, execute: Execute, *, cancelled: Cancelled = lambda: False
    ) -> None:
        self._execute = execute
        self._cancelled = cancelled

    def run(self, profile: DeviceProfile) -> tuple[DiagnosticResult, ...]:
        results: list[DiagnosticResult] = []
        sim_locked = False
        for command in profile.diagnostic_commands:
            if self._cancelled():
                results.append(
                    DiagnosticResult(
                        command.id, DiagnosticState.SKIPPED, (), "Run cancelled."
                    )
                )
                break
            if sim_locked and command.id in {"sms-storage", "operator"}:
                results.append(
                    DiagnosticResult(
                        command.id, DiagnosticState.SKIPPED, (), "SIM is locked."
                    )
                )
                continue
            exchange = self._execute(command)
            result = self._interpret(command, exchange)
            results.append(result)
            sim_locked = sim_locked or b"+CPIN: SIM PIN" in result.evidence
        return tuple(results)

    @staticmethod
    def _interpret(command: CatalogCommand, exchange: AtExchange) -> DiagnosticResult:
        evidence = exchange.response_lines + (
            (exchange.final_result,) if exchange.final_result else ()
        )
        if exchange.outcome is not ExchangeOutcome.COMPLETED:
            return DiagnosticResult(
                command.id,
                DiagnosticState.UNKNOWN,
                evidence,
                "Check the serial connection.",
            )
        if exchange.final_result != b"OK":
            return DiagnosticResult(
                command.id,
                DiagnosticState.UNSUPPORTED,
                evidence,
                "Check command applicability.",
            )
        if b"+CPIN: SIM PIN" in evidence:
            return DiagnosticResult(
                command.id,
                DiagnosticState.ATTENTION,
                evidence,
                "Enter the PIN explicitly.",
            )
        if any(
            b"99,99" in line or b",2" in line or b"No Service" in line
            for line in evidence
        ):
            return DiagnosticResult(
                command.id,
                DiagnosticState.ATTENTION,
                evidence,
                "Check registration and coverage manually.",
            )
        return DiagnosticResult(
            command.id, DiagnosticState.OK, evidence, "No action required."
        )
