"""Record a real demo session: runs six questions through cli.py and writes
demo/transcript.md and demo/transcript.json verbatim from the actual output.
Nothing here is hand-edited; re-run with `make demo`."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
QUESTIONS = [
    "How many days of PTO do I get?",
    "I'm going to the autumn retreat, how do I book my flight and when?",
    "What's the hotel cap for a conference in London?",
    "Can I spend $400 on a standing desk for my home office?",
    "What is the office wifi password?",
    "What's the limit?",
]


def main() -> None:
    runs = []
    for q in QUESTIONS:
        print(f"asking: {q}", file=sys.stderr)
        out = subprocess.run([sys.executable, str(HERE.parent / "cli.py"), "--json", q],
                             capture_output=True, text=True, check=True, timeout=200).stdout
        runs.append(json.loads(out))
    (HERE / "transcript.json").write_text(json.dumps(runs, indent=2))
    md = [f"# Demo transcript ({time.strftime('%Y-%m-%d', time.gmtime())})", "",
          "Recorded by `demo/record.py` through `python cli.py --json ...`; answers are verbatim.",
          f"Backend `{runs[0]['backend']}`; cost is what Claude Code reported (`total_cost_usd`).", ""]
    for i, r in enumerate(runs, 1):
        md += [f"## {i}. {r['question']}", "", "> " + r["answer"].replace("\n", "\n> "), "",
               f"Sources: {', '.join(r['sources']) or 'none'} · cost ${r['cost_usd']:.4f} · "
               f"{r['num_turns']} turns · {r['duration_ms'] / 1000:.1f}s", ""]
    total = sum(r["cost_usd"] or 0 for r in runs)
    md.append(f"Total for 6 questions: ${total:.4f} (average ${total / len(runs):.4f}).")
    (HERE / "transcript.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main()
