"""Slack handler against a fake client: threading, reactions, feedback log."""
import json

from helper.brain import Answer
from helper.slack_app import Helper


class FakeClient:
    def __init__(self, replies=None):
        self.calls = []
        self.replies = replies or []

    def reactions_add(self, **kw): self.calls.append(("reactions_add", kw))
    def reactions_remove(self, **kw): self.calls.append(("reactions_remove", kw))
    def conversations_replies(self, **kw):
        self.calls.append(("conversations_replies", kw))
        return {"messages": self.replies}
    def chat_postMessage(self, **kw):
        self.calls.append(("chat_postMessage", kw))
        return {"ts": "200.1"}


def fake_brain(question, thread_context=None):
    fake_brain.seen = (question, thread_context)
    return Answer(text="You get 28 days.", sources=["pto-policy.md"], cost_usd=0.01, cost_source="reported")


def test_mention_is_answered_in_thread_with_sources_and_eyes(tmp_path):
    h = Helper(brain=fake_brain, feedback_path=tmp_path / "f.jsonl", bot_user_id="UBOT")
    client = FakeClient()
    h.handle_message({"channel": "C1", "ts": "100.5", "text": "<@UBOT> how many PTO days?", "user": "U1"}, client)
    names = [c[0] for c in client.calls]
    assert names == ["reactions_add", "chat_postMessage", "reactions_remove"]
    post = client.calls[1][1]
    assert post["thread_ts"] == "100.5" and "28 days" in post["text"] and "`pto-policy.md`" in post["text"]
    assert fake_brain.seen == ("how many PTO days?", None)
    assert client.calls[0][1]["name"] == "eyes"


def test_thread_reply_passes_earlier_messages_as_context(tmp_path):
    h = Helper(brain=fake_brain, feedback_path=tmp_path / "f.jsonl", bot_user_id="UBOT")
    client = FakeClient(replies=[{"ts": "1.0", "text": "<@UBOT> PTO?"}, {"ts": "1.5", "text": "28 days", "bot_id": "B1"},
                                 {"ts": "2.0", "text": "and carry-over?"}])
    h.handle_message({"channel": "C1", "ts": "2.0", "thread_ts": "1.0", "text": "and carry-over?"}, client)
    assert fake_brain.seen == ("and carry-over?", ["User: PTO?", "Helper: 28 days"])


def test_bot_and_edited_messages_are_ignored(tmp_path):
    h = Helper(brain=fake_brain, feedback_path=tmp_path / "f.jsonl")
    client = FakeClient()
    h.handle_message({"channel": "C1", "ts": "1", "text": "x", "bot_id": "B9"}, client)
    h.handle_message({"channel": "C1", "ts": "1", "text": "x", "subtype": "message_changed"}, client)
    assert client.calls == []


def test_brain_error_still_replies_and_clears_eyes(tmp_path):
    def broken(question, thread_context=None):
        raise RuntimeError("claude exited 1")
    h = Helper(brain=broken, feedback_path=tmp_path / "f.jsonl")
    client = FakeClient()
    h.handle_message({"channel": "C1", "ts": "1", "text": "hi"}, client)
    assert "could not answer" in client.calls[1][1]["text"] and client.calls[-1][0] == "reactions_remove"


def test_thumbs_reaction_on_own_reply_is_logged(tmp_path):
    path = tmp_path / "f.jsonl"
    h = Helper(brain=fake_brain, feedback_path=path, bot_user_id="UBOT")
    h.handle_message({"channel": "C1", "ts": "100.5", "text": "PTO?"}, FakeClient())
    assert h.handle_reaction({"reaction": "-1", "user": "U2", "item_user": "UBOT", "item": {"channel": "C1", "ts": "200.1"}})
    assert h.handle_reaction({"reaction": "+1", "user": "U2", "item_user": "UOTHER", "item": {"channel": "C1", "ts": "200.1"}}) is None
    assert h.handle_reaction({"reaction": "tada", "user": "U2", "item_user": "UBOT", "item": {"channel": "C1", "ts": "200.1"}}) is None
    rec = json.loads(path.read_text().strip())
    assert rec["rating"] == "down" and rec["question"] == "PTO?" and rec["sources"] == ["pto-policy.md"]
