"""Eval file parsing and the grading rules."""
import pytest
import yaml

from helper.brain import Answer
from run_evals import grade, load_questions


def test_questions_file_has_8_answerable_2_refusals_2_clarifications():
    qs = load_questions()
    assert len(qs) == 12 and len({q["id"] for q in qs}) == 12
    assert sum(1 for q in qs if q.get("expect")) == 8
    assert sum(1 for q in qs if q.get("must_refuse")) == 2
    assert sum(1 for q in qs if q.get("must_clarify")) == 2


def test_malformed_question_is_rejected(tmp_path):
    bad = tmp_path / "q.yaml"
    bad.write_text(yaml.safe_dump([{"id": "x", "question": "?", "expect": ["1"], "must_refuse": True}]))
    with pytest.raises(ValueError):
        load_questions(bad)


def test_grade_rules():
    q = {"expect": ["28", "31 March"], "source": "pto-policy.md"}
    assert grade(q, Answer(text="28 days, use by 31 march", sources=["pto-policy.md"]))[0]
    assert grade(q, Answer(text="28 days", sources=["pto-policy.md"])) == (False, "missing ['31 March']")
    assert not grade(q, Answer(text="28 days, 31 March", sources=["travel-booking.md"]))[0]
    assert grade({"must_refuse": True}, Answer(text="I don't know, ask #it-help"))[0]
    assert not grade({"must_refuse": True}, Answer(text="It is 42."))[0]
    assert grade({"must_clarify": True}, Answer(text="Which limit do you mean?"))[0]
    assert not grade({"must_clarify": True}, Answer(text="I don't know?"))[0]
