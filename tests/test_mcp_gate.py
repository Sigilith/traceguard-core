import pytest

from traceguard_core.engine import evaluate_call, parse_allowed_actions


def test_allowlist_is_exact():
    assert evaluate_call("read_logs", {"limit": 1}, ["read_logs"])
    assert not evaluate_call("read_logs_extra", {"limit": 1}, ["read_logs"])


@pytest.mark.parametrize(
    "tool,args",
    [("", {}), (None, {}), ("read_logs", None), ("read_logs", []), ("read_logs", {1: "bad"})],
)
def test_malformed_requests_fail_closed(tool, args):
    assert not evaluate_call(tool, args, ["read_logs"])


def test_missing_configuration_denies_every_action(monkeypatch):
    monkeypatch.delenv("TRACEGUARD_ALLOWED_ACTIONS", raising=False)
    assert parse_allowed_actions() == frozenset()
    assert not evaluate_call("read_logs", {}, None)


def test_invalid_configuration_is_rejected_and_runtime_denies(monkeypatch):
    monkeypatch.setenv("TRACEGUARD_ALLOWED_ACTIONS", "not-json")
    with pytest.raises(ValueError):
        parse_allowed_actions()
    assert not evaluate_call("read_logs", {}, None)


def test_configuration_requires_nonempty_string_array():
    assert parse_allowed_actions('["read_logs", "inspect"]') == frozenset({"read_logs", "inspect"})
    with pytest.raises(ValueError):
        parse_allowed_actions('["read_logs", 3]')
