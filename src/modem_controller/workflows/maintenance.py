"""Explicit, one-shot execution of reviewed state-changing AT actions."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from modem_controller.catalog.models import (
    CatalogCommand,
    CommandKind,
    CommandUnavailableError,
    RiskLevel,
)
from modem_controller.protocol.at_session import AtExchange, ExchangeOutcome


class MaintenanceOutcome(str, Enum):
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class MaintenancePreview:
    command_id: str
    risk: RiskLevel
    risk_summary: str
    contains_secret: bool


@dataclass(frozen=True, slots=True)
class MaintenanceResult:
    command_id: str
    outcome: MaintenanceOutcome
    evidence: tuple[bytes, ...]
    session_invalidated: bool
    capture_gap: str | None
    next_action: str


Execute = Callable[[bytes], AtExchange]


class MaintenanceRunner:
    """Runs one explicitly confirmed action and never retries it automatically."""

    def __init__(self, execute: Execute, *, terminator: bytes = b"\r") -> None:
        if terminator not in {b"\r", b"\n", b"\r\n"}:
            raise ValueError("terminator must be CR, LF, or CRLF")
        self._execute = execute
        self._terminator = terminator

    @staticmethod
    def preview(command: CatalogCommand) -> MaintenancePreview:
        MaintenanceRunner._validate_command(command)
        return MaintenancePreview(
            command.id,
            command.risk,
            command.help_text,
            any(parameter.secret for parameter in command.parameters),
        )

    def run(
        self,
        command: CatalogCommand,
        values: dict[str, str],
        *,
        confirmed: bool,
    ) -> MaintenanceResult:
        preview = self.preview(command)
        if not confirmed:
            return MaintenanceResult(
                command.id,
                MaintenanceOutcome.CANCELLED,
                (),
                False,
                None,
                "Review the risk preview and confirm before sending this action.",
            )

        payload = command.render(values) + self._terminator
        exchange = self._execute(payload)
        evidence = exchange.response_lines + (
            (exchange.final_result,) if exchange.final_result is not None else ()
        )
        if (
            exchange.outcome is ExchangeOutcome.COMPLETED
            and exchange.final_result == b"OK"
        ):
            outcome = MaintenanceOutcome.COMPLETED
            next_action = "Reconnect or resynchronize before another action."
        else:
            outcome = MaintenanceOutcome.INCONCLUSIVE
            next_action = "Do not retry automatically; reconnect or inspect evidence."
        capture_gap = None
        if preview.contains_secret:
            capture_gap = "Sensitive maintenance input was excluded from capture."
        return MaintenanceResult(
            command.id,
            outcome,
            evidence,
            True,
            capture_gap,
            next_action,
        )

    @staticmethod
    def _validate_command(command: CatalogCommand) -> None:
        if not command.is_visible:
            raise CommandUnavailableError("maintenance action is not verified")
        if command.kind is not CommandKind.AT:
            raise CommandUnavailableError(
                "maintenance actions must be individual AT commands"
            )
        if command.risk is RiskLevel.READ_ONLY:
            raise ValueError("read-only commands do not need maintenance confirmation")
