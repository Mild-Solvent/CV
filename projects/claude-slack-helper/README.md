# Claude in Slack helper

A Slack bot that answers staff questions ("how many PTO days do I get?") from a small internal
knowledge base, cites the document it used, and says "I don't know" when the docs do not cover it.
The brain is Claude Code run headlessly with an MCP server over the docs; the same setup staff already
use at their desks.

Built as a portfolio piece for an AI-enablement role. The organisation in the docs, "Orbit Research",
is fictional. Everything in `demo/` and `evals/last_run.md` is recorded output from real runs.

## Why this design

- **One place to maintain.** The bot is `claude -p` plus an MCP server. The skills, prompts and MCP
  servers that staff share in their own Claude Code sessions are the same objects the bot uses, so
  improving one improves both. There is no second "bot framework" to keep in sync.
- **The knowledge base is just markdown.** Adding or correcting a policy is editing a file. No
  embeddings, no index to rebuild, nothing to redeploy; the MCP server reads from disk on every call.
- **Pluggable brain.** `BRAIN=api` swaps Claude Code for the Anthropic SDK and the same tool functions.
  Useful if a team has an API key but no Claude Code seats. (Untested here, see Limitations.)
- **Small on purpose.** About 600 lines of Python plus 200 of tests. A new owner can read all of it in
  an hour, which matters more for an internal tool than features do.
- **Measured, not assumed.** `make evals` runs 12 questions through the real brain and prints a
  scorecard with cost per answer. The eval, the runbook and the feedback log are how the tool earns
  its keep or gets retired.

## Architecture

```
  Slack workspace                       this repo                               Anthropic
 ┌────────────────┐   Socket Mode   ┌───────────────────┐                   ┌──────────────┐
 │ @helper in a   │ ─────────────▶  │ helper/slack_app  │                   │              │
 │ channel or DM  │ ◀─────────────  │  (Bolt, threads,  │                   │  Claude API  │
 │ 👀 → answer    │                 │   👍/👎 → jsonl)  │                   │              │
 └────────────────┘                 └─────────┬─────────┘                   └──────▲───────┘
                                              │ answer(question, thread)           │
  Terminal                           ┌────────▼──────────┐   BRAIN=claude-code     │
 ┌────────────────┐                  │   helper/brain.py │ ───▶ claude -p ─────────┤
 │ python cli.py  │ ───────────────▶ │  system prompt,   │      --mcp-config       │
 │ evals/run_evals│                  │  source parsing,  │      --allowedTools     │
 └────────────────┘                  │  cost accounting  │   BRAIN=api             │
                                     └────────┬──────────┘ ───▶ Messages API ──────┘
                                              │ stdio (MCP) / direct import
                                     ┌────────▼──────────┐
                                     │ mcp_server/       │   list_docs()
                                     │  server.py + kb.py│   search_docs(query)
                                     └────────┬──────────┘   read_doc(name)
                                              │ reads files
                                     ┌────────▼──────────┐
                                     │ kb/*.md  (7 docs) │
                                     └───────────────────┘
```

Claude Code is launched with no built-in tools (`--tools ""`), only the three MCP tools allowed, and
`--permission-prompts none`, so the worst a prompt injection in a Slack message can do is read the
same policy docs anyone in the company can read.

## Five-minute setup

Needs Python 3.11+, and either Claude Code on `PATH` (logged in) or an `ANTHROPIC_API_KEY`.

```bash
cd projects/claude-slack-helper
make setup                                   # venv + pip install -r requirements.txt
make test                                    # 19 unit tests, no model calls, about 1 s
.venv/bin/python cli.py "How many days of PTO do I get?"
.venv/bin/python cli.py --repl               # multi-turn; earlier turns are passed as thread context
make evals                                   # 12 real questions, scorecard, writes evals/last_run.md
```

A real run of the first question (Opus 5.5, reported cost from Claude Code):

```
Full-time employees get *28 days of PTO per calendar year*, plus the public holidays of the
country you're employed in. [...] you can carry *up to 5 unused days* into next year as long
as you use them by 31 March.

Sources: pto-policy.md
Cost: $0.0451 (reported) · backend: claude-code
```

The same question cost $0.0280 in the eval run and $0.0169 in the recorded demo: the agent
sometimes reads one document and sometimes two or three before answering. The budget below uses
the average across all 18 recorded calls, not the best case.

Six more recorded questions, including a refusal and a clarifying question, are in
[`demo/transcript.md`](demo/transcript.md) (`demo/transcript.json` has the same data).

## How to add or change a doc

1. Put a markdown file in `kb/`. First line `# Title`, then an owner/channel line, then the content.
   Specific numbers and channel names make answers checkable; vague prose does not.
2. Ask it something: `.venv/bin/python cli.py "..."`. Search is keyword-based, so use the words
   staff would use in the question (the search stems "expenses"→"expense", "days"→"day").
3. Add a question with the expected fact to `evals/questions.yaml`, run `make evals`, commit the new
   `evals/last_run.md` with the doc.

Nothing to restart. The MCP server reads the folder on every call.

## How to add a Slack workspace

Not tested against a live workspace (I had none in the build environment); the handler is unit-tested
with a fake Slack client. Written against slack-bolt 1.30.

1. api.slack.com → *Create New App* → from scratch.
2. *Socket Mode* → enable. Create an app-level token with scope `connections:write` → `SLACK_APP_TOKEN`.
   Socket Mode means no public URL and no inbound firewall rule; the bot dials out.
3. *OAuth & Permissions* → bot token scopes:
   `app_mentions:read`, `chat:write`, `reactions:read`, `reactions:write`, `im:history`, `im:read`,
   `im:write`, `channels:history`, `groups:history` (the last two only so it can read the thread it is
   replying in). Install to workspace → `SLACK_BOT_TOKEN`.
4. *Event Subscriptions* → enable, subscribe to bot events `app_mention`, `message.im`, `reaction_added`.
5. *App Home* → allow users to send messages (so DMs work).
6. `cp .env.example .env`, fill in both tokens, then `set -a; source .env; set +a; make slack`.
7. Invite the bot to a channel and @mention it. Reply in the thread for follow-ups; the bot passes the
   earlier thread messages to the brain as context.

Feedback: 👍 or 👎 on a bot reply appends a line to `feedback.jsonl` with the question, the sources and
the cost, so a weekly `jq` gives you an accuracy signal without a dashboard.

## What it costs to run

All figures are `total_cost_usd` as reported by Claude Code for `claude-opus-5-5`, the default model,
across the 18 recorded calls in `evals/last_run.md` and `demo/transcript.json`:

| | |
|---|---|
| Cheapest answer (clarifying question) | $0.007 |
| Typical answer with one doc read | $0.026–0.037 |
| Average over 18 calls | **$0.025** |
| Latency | 5–10 s per answer, 2–3 model turns |
| 40 questions/day × 22 working days | **~$22 per month** |
| Same with `HELPER_MODEL=claude-sonnet-5-5` | about half (one Sonnet run in testing: $0.028 vs $0.045 for the same question on Opus) |

The number Claude Code reports is list-price API cost. If the bot runs on a Claude Team or Enterprise
seat it comes out of that seat's quota instead; the dollar figure is still the right one for deciding
whether the tool is worth it. Each call also includes a ~$0.0001 Haiku call that Claude Code makes
for its own housekeeping; it is in the reported total.

## When I would retire it

The metric is **answered-and-useful per week**: questions the bot answered (not refused) that got a 👍
or no 👎, from `feedback.jsonl`. If that is under about 15 a week for a month, the knowledge base is
either too small to matter or people have stopped asking, and the honest move is to delete the bot and
put the seven docs in a pinned Slack message. The second trip-wire is 👎 above 20% of ratings for two
weeks running: that means wrong answers, which is worse than no bot. The runbook says what to do first.

## Limitations and what is untested

- **The Slack path has never talked to Slack.** It is written against the current Bolt API and covered
  by five handler tests with a fake client, but the first live run will find something: a scope I
  missed, a payload field that differs. Budget an hour for that.
- **`BRAIN=api` is untested in this environment.** There was no `ANTHROPIC_API_KEY` here. The code
  follows the documented Messages API tool-use loop and its pure parts (cost table, source parsing) are
  tested, but it has not made a real request. Its cost figure is an estimate from the public price list,
  and is labelled "estimate" in the output.
- **Search is keyword scoring over seven files.** It is right for this size and transparent when wrong.
  Past a few dozen docs it will start missing synonyms; that is the point to add an embedding index
  behind the same `search_docs` tool, not before.
- **The eval is 12 questions with string checks.** 12/12 says the rules held on the cases I wrote, not
  that the bot is right in general. The clarification check is "did it ask a question", which a lazy
  model could game. Read the answers in `last_run.md`, not just the table.
- **Not a security boundary.** The bot has only the three read-only MCP tools, but anyone who can
  @mention it can read every doc in `kb/`. Do not put anything in `kb/` you would not post in #general.
- **Single process, in-memory map** from bot reply to question for feedback. Restart the bot and
  reactions on earlier replies are not logged. Fine for one workspace; swap for SQLite if that hurts.
- **Code size:** 604 lines of app code (the target was 600) plus ~200 of tests.

## Verification

Run on 2026-10-21 in the build environment (Python 3.13, Claude Code 2.1.305).

`make test`:

```
$ .venv/bin/python -m pytest -q
...................                                                      [100%]
19 passed in 0.65s
```

`make evals` (every row is a real model call; full answers in [`evals/last_run.md`](evals/last_run.md)):

```
[PASS] pto-days               found ['28'], cited pto-policy.md  ($0.0280, 9s)
[PASS] pto-carryover          found ['5', '31 March'], cited pto-policy.md  ($0.0280, 8s)
[PASS] expense-receipt        found ['25'], cited expense-policy.md  ($0.0364, 9s)
[PASS] travel-business        found ['8 hours'], cited travel-booking.md  ($0.0274, 8s)
[PASS] laptop-lost            found ['#it-help', '24 hours'], cited laptop-it-setup.md  ($0.0373, 9s)
[PASS] api-budget             found ['#ai-tools', '1,000'], cited ai-tool-budget.md  ($0.0302, 9s)
[PASS] data-confidential      found ['orbit-secure'], cited data-handling.md  ($0.0294, 9s)
[PASS] onboarding-probation   found ['3 months', '30'], cited onboarding-checklist.md  ($0.0259, 7s)
[PASS] refuse-wifi            said "I don't know"  ($0.0138, 10s)
[PASS] refuse-dental          said "I don't know"  ($0.0314, 10s)
[PASS] clarify-limit          asked a clarifying question  ($0.0071, 7s)
[PASS] clarify-approval       asked a clarifying question  ($0.0192, 7s)

12/12 passed · total cost $0.3141 · 102s
```

This was the first full run of the eval; the system prompt was not changed afterwards. During
development, three single questions (one answer, one refusal, one ambiguous) were run first to check
the three rules, and one early attempt used Claude Code's `--bare` flag, which fails authentication in
this environment and is therefore not used.

## How this was built

By directing a coding agent (Claude Code), not by typing the code: the brief, the checks (tests, eval,
recorded transcript) and the review were the work. The agent found that the `mcp` package on PyPI had
renamed `FastMCP` to `MCPServer` in 2.x and that `--bare` breaks auth here; both are handled in the
code and the runbook rather than worked around silently.

## Layout

```
kb/                 seven policy docs (markdown)
mcp_server/         kb.py (search/read/list) and server.py (MCP over stdio)
helper/brain.py     answer() with the claude-code and api backends
helper/slack_app.py Bolt app: mentions, DMs, threads, reactions, feedback.jsonl
cli.py              terminal front-end; --repl; --json
evals/              questions.yaml, run_evals.py, last_run.md (real)
demo/               record.py, transcript.md and transcript.json (real)
tests/              19 pytest tests, no network
RUNBOOK.md          what to do when it breaks
```
