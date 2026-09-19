"""Bounded, non-destructive probing of serial settings."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum

from modem_controller.protocol.at_session import AtExchange, ExchangeOutcome
from modem_controller.transport.serial_port import SerialSettings


class SearchPhase(str, Enum):
    QUICK = "quick"
    EXTENDED = "extended"


class SearchOutcome(str, Enum):
    CONFIRMED = "confirmed"
    INCONCLUSIVE = "inconclusive"
    CANCELLED = "cancelled"
    DISCONNECTED = "disconnected"


@dataclass(frozen=True, slots=True)
class SearchCandidate:
    """One host-side setting combination to probe with a harmless AT command."""

    settings: SerialSettings
    phase: SearchPhase


@dataclass(frozen=True, slots=True)
class SearchAttempt:
    candidate: SearchCandidate
    exchanges: tuple[AtExchange, ...]
    outcome: SearchOutcome
    explanation: str


@dataclass(frozen=True, slots=True)
class ConnectionSearchResult:
    attempts: tuple[SearchAttempt, ...]
    selected: SearchCandidate | None

    @property
    def was_cancelled(self) -> bool:
        return (
            bool(self.attempts) and self.attempts[-1].outcome is SearchOutcome.CANCELLED
        )


Probe = Callable[[SerialSettings, bytes], AtExchange]
Cancelled = Callable[[], bool]
Apply = Callable[[SerialSettings], None]
Save = Callable[[SerialSettings], None]


class ConnectionSearchRunner:
    """Evaluate supplied serial settings without reconfiguring the modem itself."""

    def __init__(
        self,
        probe: Probe,
        *,
        cancelled: Cancelled = lambda: False,
        terminator: bytes = b"\r",
        confirmations_required: int = 2,
    ) -> None:
        if terminator not in {b"\r", b"\n", b"\r\n"}:
            raise ValueError("terminator must be CR, LF, or CRLF")
        if confirmations_required < 2:
            raise ValueError("at least two confirmations are required")
        self._probe = probe
        self._cancelled = cancelled
        self._command = b"AT" + terminator
        self._confirmations_required = confirmations_required

    @staticmethod
    def quick_candidates(port: str) -> tuple[SearchCandidate, ...]:
        return tuple(
            SearchCandidate(
                SerialSettings(port=port, baud_rate=baud_rate), SearchPhase.QUICK
            )
            for baud_rate in (9600, 19200, 38400, 57600, 115200)
        )

    def run(self, candidates: tuple[SearchCandidate, ...]) -> ConnectionSearchResult:
        attempts: list[SearchAttempt] = []
        for candidate in candidates:
            exchanges: list[AtExchange] = []
            for _ in range(self._confirmations_required):
                if self._cancelled():
                    attempts.append(
                        SearchAttempt(
                            candidate,
                            tuple(exchanges),
                            SearchOutcome.CANCELLED,
                            "Search cancelled before another probe was sent.",
                        )
                    )
                    return ConnectionSearchResult(tuple(attempts), None)
                exchange = self._probe(candidate.settings, self._command)
                exchanges.append(exchange)
                if exchange.outcome is ExchangeOutcome.DISCONNECTED:
                    attempts.append(
                        SearchAttempt(
                            candidate,
                            tuple(exchanges),
                            SearchOutcome.DISCONNECTED,
                            "The port disconnected while its settings were probed.",
                        )
                    )
                    return ConnectionSearchResult(tuple(attempts), None)
                if not self._is_confirmation(exchange):
                    break
            if len(exchanges) == self._confirmations_required and all(
                self._is_confirmation(exchange) for exchange in exchanges
            ):
                attempt = SearchAttempt(
                    candidate,
                    tuple(exchanges),
                    SearchOutcome.CONFIRMED,
                    "Two independent AT replies confirmed these host-side settings.",
                )
                return ConnectionSearchResult(tuple((*attempts, attempt)), candidate)
            attempts.append(
                SearchAttempt(
                    candidate,
                    tuple(exchanges),
                    SearchOutcome.INCONCLUSIVE,
                    "No repeated, command-correlated AT response was observed.",
                )
            )
        return ConnectionSearchResult(tuple(attempts), None)

    @staticmethod
    def use(result: ConnectionSearchResult, apply: Apply) -> SerialSettings:
        """Apply only a repeated-confirmed candidate; saving is a separate action."""

        if result.selected is None:
            raise ValueError("an inconclusive search result cannot be used")
        settings = result.selected.settings
        apply(settings)
        return settings

    @staticmethod
    def save(result: ConnectionSearchResult, save: Save) -> SerialSettings:
        """Persist only a repeated-confirmed candidate after explicit caller intent."""

        if result.selected is None:
            raise ValueError("an inconclusive search result cannot be saved")
        settings = result.selected.settings
        save(settings)
        return settings

    def _is_confirmation(self, exchange: AtExchange) -> bool:
        return (
            exchange.command == self._command
            and exchange.outcome is ExchangeOutcome.COMPLETED
            and exchange.final_result == b"OK"
        )
