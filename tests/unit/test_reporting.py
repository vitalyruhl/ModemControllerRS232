from datetime import UTC, datetime

import pytest

from modem_controller.transport.capture import CaptureDirection, CaptureRecord
from modem_controller.workflows.diagnostics import DiagnosticResult, DiagnosticState
from modem_controller.workflows.reporting import export_raw_capture, render_report


def test_report_redacts_phone_numbers_and_paths() -> None:
    result = DiagnosticResult(
        "identity",
        DiagnosticState.OK,
        (b"IMEI 123456789012345 +491234567",),
        "Check C:\\Users\\Name",
    )
    report = render_report((result,), {"path": "C:\\Users\\Name", "port": "COM7"})
    assert "123456789012345" not in str(report)
    assert "C:\\Users\\Name" not in str(report)


def test_raw_export_requires_confirmation(tmp_path) -> None:
    record = CaptureRecord(
        datetime(2026, 9, 19, tzinfo=UTC), CaptureDirection.RECEIVED, b"AT\r"
    )
    with pytest.raises(PermissionError):
        export_raw_capture(tmp_path / "raw.bin", (record,), confirmed=False)
    export_raw_capture(tmp_path / "raw.bin", (record,), confirmed=True)
    assert (tmp_path / "raw.bin").read_bytes() == b"AT\r"
