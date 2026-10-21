"""Run evals/questions.yaml through the brain and print a scorecard.

    python evals/run_evals.py            # all questions
    python evals/run_evals.py pto-days   # one id, while iterating on the prompt

Writes evals/last_run.md. Rules are deliberately simple string checks: they catch
regressions and cost drift, not nuance. A human should still read the answers.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from helper.brain import DEFAULT_MODEL, Answer, answer  # noqa: E402

HERE = Path(__file__).resolve().parent


def load_questions(path: Path = HERE / "questions.yaml") -> list[dict]:
    qs = yaml.safe_load(path.read_text())
    for q in qs:
        kinds = [k for k in ("expect", "must_refuse", "must_clarify") if q.get(k)]
        if len(kinds) != 1:
            raise ValueError(f"{q.get('id')}: needs exactly one of expect/must_refuse/must_clarify")
    return qs


def grade(q: dict, a: Answer) -> tuple[bool, str]:
    """Return (passed, reason). Pure so tests can cover it without a model."""
    text = a.text.lower()
    if q.get("must_refuse"):
        return a.refused, "said \"I don't know\"" if a.refused else "answered instead of refusing"
    if q.get("must_clarify"):
        ok = "?" in a.text and not a.refused
        return ok, "asked a clarifying question" if ok else "did not ask a question"
    missing = [s for s in q["expect"] if s.lower() not in text]
    if missing:
        return False, f"missing {missing}"
    if q.get("source") and q["source"] not in a.sources:
        return False, f"cited {a.sources or 'nothing'}, expected {q['source']}"
    return True, f"found {q['expect']}, cited {q['source']}"


def run(ids: list[str] | None = None) -> int:
    rows, total_cost, started = [], 0.0, time.time()
    for q in load_questions():
        if ids and q["id"] not in ids:
            continue
        t0 = time.time()
        try:
            a = answer(q["question"])
            passed, reason = grade(q, a)
        except Exception as exc:  # noqa: BLE001 - a crash is a failed row, not a crashed run
            a, passed, reason = Answer(text=f"ERROR: {exc}"), False, f"error: {exc}"
        total_cost += a.cost_usd or 0.0
        rows.append((q, a, passed, reason, time.time() - t0))
        print(f"[{'PASS' if passed else 'FAIL'}] {q['id']:<22} {reason}  (${a.cost_usd or 0:.4f}, {rows[-1][4]:.0f}s)")
    if not rows:
        print(f"no questions matched {ids}; known ids: {[q['id'] for q in load_questions()]}")
        return 2
    n_pass = sum(1 for r in rows if r[2])
    print(f"\n{n_pass}/{len(rows)} passed · total cost ${total_cost:.4f} · {time.time() - started:.0f}s")
    _write_report(rows, n_pass, total_cost)
    return 0 if n_pass == len(rows) else 1


def _write_report(rows, n_pass: int, total_cost: float) -> None:
    lines = [f"# Eval run {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}", "",
             f"Backend: `{rows[0][1].backend or 'n/a'}` · model: `{DEFAULT_MODEL}` · "
             f"**{n_pass}/{len(rows)} passed** · total cost **${total_cost:.4f}** "
             f"(cost source: {rows[0][1].cost_source})", "",
             "| # | id | result | check | cost | time |", "|---|---|---|---|---|---|"]
    for i, (q, a, passed, reason, secs) in enumerate(rows, 1):
        lines.append(f"| {i} | {q['id']} | {'PASS' if passed else 'FAIL'} | {reason} | ${a.cost_usd or 0:.4f} | {secs:.0f}s |")
    lines += ["", "## Answers", ""]
    for q, a, passed, reason, _ in rows:
        lines += [f"### {q['id']} - {'PASS' if passed else 'FAIL'}", f"**Q:** {q['question']}", "",
                  a.text.replace("\n", "\n> ").join(["> ", ""]), "",
                  f"Sources: {', '.join(a.sources) or 'none'}", ""]
    (HERE / "last_run.md").write_text("\n".join(lines))


if __name__ == "__main__":
    sys.exit(run(sys.argv[1:] or None))
