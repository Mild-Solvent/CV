"""Slack front-end for the helper (Bolt, Socket Mode: no public URL needed).

Behaviour: answers @mentions in channels and direct messages, always replies in a
thread, reacts with :eyes: while thinking, appends a Sources line, and logs
:+1: / :-1: reactions on its own replies to feedback.jsonl.

    python -m helper.slack_app          # needs SLACK_BOT_TOKEN and SLACK_APP_TOKEN
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any, Callable

from helper.brain import Answer, answer

log = logging.getLogger("orbit-helper")
FEEDBACK_PATH = Path(os.environ.get("FEEDBACK_PATH", Path(__file__).resolve().parent.parent / "feedback.jsonl"))
RATINGS = {"+1": "up", "thumbsup": "up", "-1": "down", "thumbsdown": "down"}


class Helper:
    """All the Slack logic, with the Slack client and the brain injected so tests can fake them."""

    def __init__(self, brain: Callable[..., Answer] = answer, feedback_path: Path = FEEDBACK_PATH,
                 bot_user_id: str | None = None) -> None:
        self.brain = brain
        self.feedback_path = feedback_path
        self.bot_user_id = bot_user_id
        self.posted: dict[tuple[str, str], dict[str, Any]] = {}   # (channel, ts) -> what we answered

    @staticmethod
    def format_reply(a: Answer) -> str:
        sources = ", ".join(f"`{s}`" for s in a.sources) if a.sources else "none"
        return f"{a.text}\n\n_Sources: {sources}_\n_Was this useful? React :+1: or :-1: to this message._"

    def handle_message(self, event: dict[str, Any], client: Any) -> None:
        if event.get("bot_id") or event.get("subtype"):           # ignore bots, edits, joins
            return
        channel, ts = event["channel"], event["ts"]
        thread_ts = event.get("thread_ts", ts)
        question = re.sub(r"<@[A-Z0-9]+>", "", event.get("text", "")).strip()
        if not question:
            return
        client.reactions_add(channel=channel, name="eyes", timestamp=ts)
        try:
            context = self._thread_context(client, channel, thread_ts, ts) if "thread_ts" in event else None
            a = self.brain(question, thread_context=context)
            res = client.chat_postMessage(channel=channel, thread_ts=thread_ts, text=self.format_reply(a))
            self.posted[(channel, res["ts"])] = {"question": question, "sources": a.sources, "cost_usd": a.cost_usd}
        except Exception:                                           # noqa: BLE001 - never leave a user hanging
            log.exception("brain failed for %r", question)
            client.chat_postMessage(channel=channel, thread_ts=thread_ts,
                                    text="Sorry, I hit an error and could not answer. Please ask in #it-help.")
        finally:
            client.reactions_remove(channel=channel, name="eyes", timestamp=ts)

    def _thread_context(self, client: Any, channel: str, thread_ts: str, current_ts: str) -> list[str]:
        replies = client.conversations_replies(channel=channel, ts=thread_ts, limit=20).get("messages", [])
        return [("Helper: " if m.get("bot_id") else "User: ") + re.sub(r"<@[A-Z0-9]+>", "", m.get("text", "")).strip()
                for m in replies if m.get("ts") != current_ts]

    def handle_reaction(self, event: dict[str, Any]) -> dict[str, Any] | None:
        rating = RATINGS.get(event.get("reaction", ""))
        item = event.get("item", {})
        key = (item.get("channel"), item.get("ts"))
        if rating is None or event.get("item_user") != self.bot_user_id or key not in self.posted:
            return None
        record = {"time": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "rating": rating,
                  "user": event.get("user"), "channel": key[0], "ts": key[1], **self.posted[key]}
        with self.feedback_path.open("a") as f:
            f.write(json.dumps(record) + "\n")
        return record


def build_app(helper: Helper | None = None):
    """Wire the handler into a Bolt App. Kept separate from main() so tests can import without tokens."""
    from slack_bolt import App

    app = App(token=os.environ["SLACK_BOT_TOKEN"])
    helper = helper or Helper(bot_user_id=app.client.auth_test()["user_id"])

    @app.event("app_mention")
    def on_mention(event, client):
        helper.handle_message(event, client)

    @app.event("message")
    def on_message(event, client):
        if event.get("channel_type") == "im":                       # DMs only; channel chatter needs an @mention
            helper.handle_message(event, client)

    @app.event("reaction_added")
    def on_reaction(event):
        helper.handle_reaction(event)

    return app


def main() -> None:
    from slack_bolt.adapter.socket_mode import SocketModeHandler

    logging.basicConfig(level=logging.INFO)
    SocketModeHandler(build_app(), os.environ["SLACK_APP_TOKEN"]).start()


if __name__ == "__main__":
    main()
