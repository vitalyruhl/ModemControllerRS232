import pytest

from modem_controller.protocol.framing import AtFramer, FrameKind


def test_framer_handles_split_and_merged_cr_lf_and_crlf_lines() -> None:
    framer = AtFramer()

    assert framer.feed(b"AT\r") == ()
    frames = framer.feed(b"\nOK\r+CSQ: 20,99\nERROR\r\n")

    assert [(frame.data, frame.terminator) for frame in frames] == [
        (b"AT", b"\r\n"),
        (b"OK", b"\r"),
        (b"+CSQ: 20,99", b"\n"),
        (b"ERROR", b"\r\n"),
    ]


def test_framer_emits_prompt_without_a_newline_and_preserves_invalid_bytes() -> None:
    framer = AtFramer()

    frames = framer.feed(b"\r\n> \xff\r\n")

    assert [frame.kind for frame in frames] == [
        FrameKind.LINE,
        FrameKind.PROMPT,
        FrameKind.LINE,
    ]
    assert frames[1].data == b">"
    assert frames[2].data == b" \xff"


def test_framer_rejects_non_bytes_input() -> None:
    with pytest.raises(TypeError):
        AtFramer().feed("OK\r\n")  # type: ignore[arg-type]
