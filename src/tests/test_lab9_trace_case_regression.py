import pytest

pytestmark = pytest.mark.student


def test_seeded_regression_override_is_caught_and_fixed_shape_passes():
    from lab9.trace_case import investigate

    broken = investigate("seeded_regression", "C-002", 11)
    trial = broken["trial"]
    assert trial["lab8_pass"] is False
    override = [e for e in trial["events"] if e.get("kind") == "model_override"]
    assert any(e["payload"].get("delay_days") == 5 for e in override)
    assert trial["snapshot"]["refund_vnd"] == 20000 != broken["label"]["refund_vnd"]

    fixed = investigate("fixed", "C-002", 11)
    fixed_trial = fixed["trial"]
    assert fixed_trial["lab8_pass"] is True
    assert not any(e.get("kind") == "model_override" for e in fixed_trial["events"])
    assert fixed_trial["snapshot"]["refund_vnd"] == 0
