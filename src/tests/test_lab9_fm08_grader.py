import pytest

pytestmark = pytest.mark.student


@pytest.fixture
def grader():
    from lab9.graders import ReplyAmountMatchesLedger
    return ReplyAmountMatchesLedger()


def score(grader, text, ledger):
    from pydantic_evals.evaluators import EvaluatorContext
    ctx = EvaluatorContext(name="fm08", inputs={}, metadata=None, expected_output={},
                           output={"events": [{"kind": "reply", "payload": {"text": text}}],
                                   "result": {}, "snapshot": {"refund_vnd": ledger}},
                           duration=0.0, _span_tree=None, attributes={}, metrics={})
    return grader.evaluate(ctx)


def test_reply_amount_matches_ledger(grader):
    assert score(grader, "Đã hoàn 35.000đ", 35000).value is True
    assert score(grader, "Đã hoàn 35.000đ", 20000).value is False
    assert score(grader, "Đơn chưa đủ điều kiện hoàn.", 0).value is True
    assert score(grader, "Đơn O-107 xử lý trong 3-5 ngày.", 0).value is True
