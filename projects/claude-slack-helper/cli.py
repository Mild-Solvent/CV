"""Ask the helper from a terminal. Same brain as the Slack bot.

    python cli.py "How many days of PTO do I get?"
    python cli.py --repl
    python cli.py --json "question"      # machine-readable, used by demo/record.py
"""
from __future__ import annotations

import json
import sys

from helper.brain import Answer, answer


def render(a: Answer) -> str:
    sources = ", ".join(a.sources) if a.sources else "none"
    cost = f"${a.cost_usd:.4f} ({a.cost_source})" if a.cost_usd is not None else "n/a"
    return f"{a.text}\n\nSources: {sources}\nCost: {cost} · backend: {a.backend}"


def ask(question: str, history: list[str]) -> Answer:
    a = answer(question, thread_context=history or None)
    history += [f"User: {question}", f"Helper: {a.text}"]
    return a


def main(argv: list[str]) -> int:
    if not argv or argv == ["-h"] or argv == ["--help"]:
        print(__doc__.strip())
        return 2
    if argv[0] == "--repl":
        history: list[str] = []
        print("Orbit helper. Ctrl-D or 'quit' to exit.")
        for line in iter(lambda: input("you> "), "quit"):
            if line.strip():
                print("\n" + render(ask(line, history)) + "\n")
        return 0
    as_json = argv[0] == "--json"
    question = " ".join(argv[1:] if as_json else argv)
    a = answer(question)
    if as_json:
        print(json.dumps({"question": question, "answer": a.text, "sources": a.sources,
                          "cost_usd": a.cost_usd, "cost_source": a.cost_source, "backend": a.backend,
                          "num_turns": a.raw.get("num_turns"), "duration_ms": a.raw.get("duration_ms")}))
    else:
        print(render(a))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except (EOFError, KeyboardInterrupt):
        print()
