import pytest

from traceguard import AXIOMOSEvaluator, AsyncEvidenceLedger, TraceGuard


@pytest.mark.parametrize("value", [None, 1, [], {}])
def test_non_string_action_fails_closed(value):
    guard = TraceGuard(allowed_actions=["read_logs"])
    assert guard.evaluate_action(value) == "BLOCK"


def test_src_package_wins_over_legacy_root_script():
    from pathlib import Path
    import traceguard

    package_file = Path(traceguard.__file__).resolve()
    assert package_file.parent.name == "traceguard"
    assert "src" in package_file.parts
    assert AXIOMOSEvaluator is not None
    assert AsyncEvidenceLedger is not None
