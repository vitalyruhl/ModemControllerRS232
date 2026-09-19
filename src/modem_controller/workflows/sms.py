"""Explicit text-mode SMS status, reading, and one-message sending."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import timedelta
from enum import Enum

from modem_controller.protocol.at_session import AtExchange, AtSession, ExchangeOutcome

_RECIPIENT = re.compile(r"\+?[0-9]{3,15}")


class SmsOutcome(str, Enum):
    CANCELLED = "cancelled"
    SENT = "sent"
    INDETERMINATE = "indeterminate"


class SmsConfirmationRequiredError(ValueError):
    """Raised when a potentially state-changing SMS read was not confirmed."""


@dataclass(frozen=True, slots=True)
class SmsMessage:
    recipient: str
    body: str

    def __post_init__(self) -> None:
        if _RECIPIENT.fullmatch(self.recipient) is None:
            raise ValueError("recipient must contain 3 to 15 digits with an optional +")
        if not self.body or len(self.body) > 160:
            raise ValueError("text-mode SMS body must contain 1 to 160 characters")
        if not self.body.isascii() or any(
            ord(character) < 32 for character in self.body
        ):
            raise ValueError("only printable ASCII text-mode SMS bodies are supported")


@dataclass(frozen=True, slots=True)
class SmsSendResult:
    outcome: SmsOutcome
    evidence: tuple[bytes, ...]
    next_action: str


class SmsInspector:
    """Builds explicit SMS queries without deleting or changing configuration."""

    @staticmethod
    def status_commands() -> tuple[bytes, ...]:
        return (b"AT+CMGF?\r", b"AT+CSCS?\r", b"AT+CPMS?\r")

    @staticmethod
    def read_message(index: int, *, confirmed: bool) -> bytes:
        if index <= 0:
            raise ValueError("SMS index must be positive")
        if not confirmed:
            raise SmsConfirmationRequiredError(
                "reading an SMS may change its read/unread state"
            )
        return f"AT+CMGR={index}\r".encode("ascii")


class SmsSendWorkflow:
    """Sends exactly one confirmed text-mode SMS and never retries delivery."""

    def __init__(self, session: AtSession, *, completion_timeout: timedelta) -> None:
        if completion_timeout.total_seconds() <= 0:
            raise ValueError("completion_timeout must be positive")
        self._session = session
        self._completion_timeout = completion_timeout
        self._message: SmsMessage | None = None
        self._submitted = False

    def begin(self, message: SmsMessage, *, confirmed: bool) -> SmsSendResult | None:
        if not confirmed:
            return SmsSendResult(
                SmsOutcome.CANCELLED,
                (),
                "Review the recipient and text, then confirm before sending.",
            )
        self._message = message
        self._submitted = False
        self._session.start(
            f'AT+CMGS="{message.recipient}"\r'.encode("ascii"),
            timeout=self._completion_timeout,
            sensitive=True,
        )
        return None

    def poll(self) -> SmsSendResult | None:
        completed = self._session.poll()
        if completed is not None:
            return self._result(completed)
        active = self._session.active_exchange
        if active is not None and active.prompt_received and not self._submitted:
            message = self._message
            if message is None:
                raise RuntimeError("SMS message is missing")
            self._session.submit_prompt_payload(
                message.body.encode("ascii") + b"\x1a", sensitive=True
            )
            self._submitted = True
        return None

    def cancel(self) -> SmsSendResult:
        return self._result(self._session.cancel())

    @staticmethod
    def _result(exchange: AtExchange) -> SmsSendResult:
        evidence = exchange.response_lines + (
            (exchange.final_result,) if exchange.final_result is not None else ()
        )
        if (
            exchange.outcome is ExchangeOutcome.COMPLETED
            and exchange.final_result == b"OK"
        ):
            return SmsSendResult(
                SmsOutcome.SENT,
                evidence,
                (
                    "Delivery acknowledgement recorded; no message will be resent "
                    "automatically."
                ),
            )
        if exchange.outcome is ExchangeOutcome.CANCELLED:
            return SmsSendResult(
                SmsOutcome.CANCELLED,
                evidence,
                "Send cancelled; reconnect or resynchronize before another action.",
            )
        return SmsSendResult(
            SmsOutcome.INDETERMINATE,
            evidence,
            "Delivery is indeterminate; do not resend automatically.",
        )
