"""Privacy-aware rendering and export of diagnostic evidence."""

from __future__ import annotations

import json
import re
from pathlib import Path

from modem_controller.transport.capture import CaptureRecord
from modem_controller.workflows.diagnostics import DiagnosticResult

_SENSITIVE = re.compile(r"(\+?\d{6,}|\b\d{14,}\b|[A-Za-z]:\\[^\s]+)")


def redact(value: str) -> str:
    return _SENSITIVE.sub("<redacted>", value)


def render_report(
    results: tuple[DiagnosticResult, ...], settings: dict[str, str]
) -> dict[str, object]:
    return {
        "settings": {key: redact(value) for key, value in settings.items()},
        "results": [
            {
                "command": result.command_id,
                "state": result.state.value,
                "evidence": [
                    redact(line.decode("utf-8", errors="replace"))
                    for line in result.evidence
                ],
                "next_check": result.next_check,
            }
            for result in results
        ],
    }


def export_report(
    destination: Path,
    results: tuple[DiagnosticResult, ...],
    settings: dict[str, str],
) -> None:
    destination.write_text(
        json.dumps(render_report(results, settings), indent=2) + "\n",
        encoding="utf-8",
    )


def export_raw_capture(
    destination: Path, records: tuple[CaptureRecord, ...], *, confirmed: bool
) -> None:
    if not confirmed:
        raise PermissionError("raw capture export requires explicit confirmation")
    destination.write_bytes(b"".join(record.data for record in records))
