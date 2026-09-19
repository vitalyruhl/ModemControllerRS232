from datetime import UTC, datetime

import pytest

from modem_controller.transport.capture import (
    CaptureBuffer,
    CaptureDirection,
    CaptureRecord,
)


def test_capture_buffer_preserves_accepted_records_without_eviction() -> None:
    buffer = CaptureBuffer(max_records=1, max_bytes=2)
    first_record = CaptureRecord(
        timestamp=datetime(2026, 9, 19, tzinfo=UTC),
        direction=CaptureDirection.RECEIVED,
        data=b"OK",
    )

    assert buffer.append(first_record).accepted

    result = buffer.append(
        CaptureRecord(
            timestamp=datetime(2026, 9, 19, tzinfo=UTC),
            direction=CaptureDirection.TRANSMITTED,
            data=b"AT",
        )
    )

    assert not result.accepted
    assert result.dropped_records == 1
    assert result.dropped_bytes == 2
    assert buffer.snapshot() == (first_record,)
    assert buffer.stored_bytes == 2
    assert buffer.dropped_records == 1
    assert buffer.dropped_bytes == 2


@pytest.mark.parametrize(
    ("max_records", "max_bytes"),
    [(0, 1), (1, 0)],
)
def test_capture_buffer_rejects_invalid_limits(
    max_records: int, max_bytes: int
) -> None:
    with pytest.raises(ValueError):
        CaptureBuffer(max_records=max_records, max_bytes=max_bytes)
