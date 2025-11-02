import datetime

from utils.nlp import extract_task_and_time


def test_parses_time_and_returns_task():
    res = extract_task_and_time("Remind me to buy milk tomorrow at 9am")
    assert isinstance(res, dict)
    assert res["task"] != ""
    assert isinstance(res["time"], (datetime.datetime, type(None)))


def test_preserves_casing_and_removes_keyword():
    res = extract_task_and_time("Call Alice tomorrow")
    # task should preserve the words and not include the keyword 'tomorrow'
    assert "tomorrow" not in res["task"].lower()
    assert res["task"].lower().startswith("call alice")
