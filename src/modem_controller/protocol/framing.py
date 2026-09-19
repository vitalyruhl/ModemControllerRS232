"""Incremental framing for the line-oriented parts of an AT byte stream."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FrameKind(str, Enum):
    LINE = "line"
    PROMPT = "prompt"


@dataclass(frozen=True, slots=True)
class AtFrame:
    """A raw response unit; decoding is deliberately left to higher layers."""

    kind: FrameKind
    data: bytes
    terminator: bytes = b""


class AtFramer:
    """Buffers partial reads and emits CR, LF, CRLF, and prompt boundaries."""

    def __init__(self) -> None:
        self._pending = bytearray()
        self._at_line_start = True

    @property
    def pending(self) -> bytes:
        return bytes(self._pending)

    def feed(self, data: bytes | bytearray | memoryview) -> tuple[AtFrame, ...]:
        """Accept arbitrary read chunks and return all complete frames in order."""

        if not isinstance(data, bytes | bytearray | memoryview):
            raise TypeError("data must be bytes-like")
        self._pending.extend(data)
        frames: list[AtFrame] = []

        while self._pending:
            if self._at_line_start and self._pending[0] == ord(">"):
                del self._pending[0]
                frames.append(AtFrame(kind=FrameKind.PROMPT, data=b">"))
                self._at_line_start = False
                continue

            delimiter_index, delimiter_size = self._find_delimiter()
            if delimiter_index is None:
                break

            line = bytes(self._pending[:delimiter_index])
            terminator = bytes(
                self._pending[delimiter_index : delimiter_index + delimiter_size]
            )
            del self._pending[: delimiter_index + delimiter_size]
            frames.append(
                AtFrame(
                    kind=FrameKind.LINE,
                    data=line,
                    terminator=terminator,
                )
            )
            self._at_line_start = True

        return tuple(frames)

    def reset(self) -> bytes:
        """Forget incomplete data and return it for diagnostic capture if needed."""

        pending = bytes(self._pending)
        self._pending.clear()
        self._at_line_start = True
        return pending

    def _find_delimiter(self) -> tuple[int | None, int]:
        for index, value in enumerate(self._pending):
            if value == ord("\r"):
                if index + 1 == len(self._pending):
                    return None, 0
                if self._pending[index + 1] == ord("\n"):
                    return index, 2
                return index, 1
            if value == ord("\n"):
                return index, 1
        return None, 0
