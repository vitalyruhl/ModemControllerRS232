from modem_controller.protocol.at_session import AtExchange, ExchangeOutcome
from modem_controller.workflows.connection_search import (
    ConnectionSearchRunner,
    SearchCandidate,
    SearchOutcome,
    SearchPhase,
)


def exchange(
    command: bytes,
    *,
    outcome: ExchangeOutcome = ExchangeOutcome.COMPLETED,
    final: bytes | None = b"OK",
) -> AtExchange:
    return AtExchange(command, 0, 1, (), (), (), (), False, outcome, final)


def test_quick_search_sends_only_repeated_at_and_allows_explicit_use_save() -> None:
    sent: list[tuple[int, bytes]] = []
    applied: list[int] = []
    saved: list[int] = []

    def probe(settings, command):
        sent.append((settings.baud_rate, command))
        return exchange(command)

    result = ConnectionSearchRunner(probe).run(
        ConnectionSearchRunner.quick_candidates("COM4")
    )

    assert [command for _, command in sent] == [b"AT\r", b"AT\r"]
    assert result.selected is not None
    assert result.selected.settings.baud_rate == 9600
    ConnectionSearchRunner.use(
        result, lambda settings: applied.append(settings.baud_rate)
    )
    ConnectionSearchRunner.save(
        result, lambda settings: saved.append(settings.baud_rate)
    )
    assert applied == [9600]
    assert saved == [9600]


def test_echo_or_stale_result_does_not_confirm_a_candidate() -> None:
    candidate = SearchCandidate(
        ConnectionSearchRunner.quick_candidates("COM4")[0].settings,
        SearchPhase.QUICK,
    )
    sent: list[bytes] = []

    def probe(settings, command):
        sent.append(command)
        return exchange(b"AT\r", final=None)

    result = ConnectionSearchRunner(probe).run((candidate,))

    assert result.selected is None
    assert result.attempts[0].outcome is SearchOutcome.INCONCLUSIVE
    assert sent == [b"AT\r"]


def test_cancel_before_probe_sends_nothing_and_cannot_be_used_or_saved() -> None:
    candidate = ConnectionSearchRunner.quick_candidates("COM4")[0]
    sent: list[bytes] = []
    runner = ConnectionSearchRunner(
        lambda settings, command: sent.append(command) or exchange(command),
        cancelled=lambda: True,
    )

    result = runner.run((candidate,))

    assert result.was_cancelled
    assert sent == []
    for action in (ConnectionSearchRunner.use, ConnectionSearchRunner.save):
        try:
            action(result, lambda settings: None)
        except ValueError:
            pass
        else:
            raise AssertionError("inconclusive results must not be applied or saved")


def test_disconnect_stops_search_without_trying_another_candidate() -> None:
    candidates = ConnectionSearchRunner.quick_candidates("COM4")[:2]
    calls = 0

    def probe(settings, command):
        nonlocal calls
        calls += 1
        return exchange(command, outcome=ExchangeOutcome.DISCONNECTED, final=None)

    result = ConnectionSearchRunner(probe).run(candidates)

    assert calls == 1
    assert result.attempts[0].outcome is SearchOutcome.DISCONNECTED
