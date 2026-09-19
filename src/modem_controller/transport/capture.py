"""Timestamped byte capture independent of terminal display formatting."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class CaptureDirection(str, Enum):
    """The direction in which bytes crossed the serial connection."""

    RECEIVED = "received"
    TRANSMITTED = "transmitted"


@dataclass(frozen=True, slots=True)
class CaptureRecord:
    """One accepted, unmodified serial byte sequence."""

    timestamp: datetime
    direction: CaptureDirection
    data: bytes

    @property
    def byte_count(self) -> int:
        return len(self.data)


@dataclass(frozen=True, slots=True)
class CaptureAppendResult:
    """The result of attempting to retain a capture record."""

    accepted: bool
    dropped_records: int = 0
    dropped_bytes: int = 0


class CaptureBuffer:
    """A bounded append-only buffer that never silently evicts accepted bytes."""

    def __init__(self, *, max_records: int, max_bytes: int) -> None:
        if max_records <= 0:
            raise ValueError("max_records must be positive")
        if max_bytes <= 0:
            raise ValueError("max_bytes must be positive")

        self._max_records = max_records
        self._max_bytes = max_bytes
        self._records: deque[CaptureRecord] = deque()
        self._stored_bytes = 0
        self._dropped_records = 0
        self._dropped_bytes = 0

    @property
    def dropped_records(self) -> int:
        return self._dropped_records

    @property
    def dropped_bytes(self) -> int:
        return self._dropped_bytes

    @property
    def stored_bytes(self) -> int:
        return self._stored_bytes

    def append(self, record: CaptureRecord) -> CaptureAppendResult:
        """Retain *record* only when doing so fits the declared limits."""

        record_size = record.byte_count
        if (
            len(self._records) >= self._max_records
            or self._stored_bytes + record_size > self._max_bytes
        ):
            self._dropped_records += 1
            self._dropped_bytes += record_size
            return CaptureAppendResult(
                accepted=False,
                dropped_records=1,
                dropped_bytes=record_size,
            )

        self._records.append(record)
        self._stored_bytes += record_size
        return CaptureAppendResult(accepted=True)

    def snapshot(self) -> tuple[CaptureRecord, ...]:
        return tuple(self._records)

    def clear(self) -> None:
        self._records.clear()
        self._stored_bytes = 0
