# Runbook: Orbit helper

What to do when the bot misbehaves. Each section: how you notice, how to confirm, how to fix.
Everything here was tried while building the project unless marked otherwise.

## 0. First 60 seconds, whatever the symptom

```bash
cd projects/claude-slack-helper
.venv/bin/python -m pytest -q                      # ~1 s, no model calls. Fails => code or deps broke.
.venv/bin/python cli.py "How many days of PTO do I get?"   # ~10 s, one model call. Fails => brain broke.
```

If the CLI answers correctly and only Slack is quiet, the problem is in Slack (section 2).
If the CLI fails, read its error: it names the layer (section 1, 3 or 5).

## 1. MCP server not starting

**You notice:** every answer is "I don't know, ask #it-help", or the CLI raises
`claude reported an error` / the JSON has `"is_error": true`, or Claude replies that it has no tools.

**Confirm:** run the server by hand; it should sit silently waiting on stdin (Ctrl-C to stop):

```bash
.venv/bin/python mcp_server/server.py
```

A traceback here is the cause. Seen in practice:
- `ModuleNotFoundError: No module named 'mcp.server.mcpserver'` → wrong `mcp` version. `make setup`.
- `No module named 'mcp'` → the bot is running with system Python, not `.venv`. `helper/brain.py`
  passes `sys.executable` into the MCP config, so start the bot with `.venv/bin/python`.
- Nothing wrong by hand, but Claude still has no tools → run the exact command the brain runs
  (`claude_code_command()` in `helper/brain.py`) with `--debug=mcp` added; the log names the
  server it failed to connect to and why.

**Fix:** correct the environment, re-run `make test`, then `make ask Q="..."`.

## 2. Slack token expired or revoked

**You notice:** the process exits at start with `invalid_auth` / `not_authed`, or Socket Mode
reconnects in a loop, or mentions get no :eyes: reaction at all.

**Confirm:**

```bash
.venv/bin/python -c "import os; from slack_sdk import WebClient; print(WebClient(token=os.environ['SLACK_BOT_TOKEN']).auth_test())"
```

`invalid_auth` → the bot token (`xoxb-`) is dead: the app was reinstalled, uninstalled, or a
workspace admin rotated tokens. `connections:write` errors on start → the app-level token
(`xapp-`) is missing that scope.

**Fix:** in api.slack.com → your app → *OAuth & Permissions*, reinstall to the workspace and copy the
new bot token; *Basic Information → App-Level Tokens* for the `xapp-` token. Update `.env`, restart.
No code changes. Untested here: this project was built without a Slack workspace.

## 3. Rate limit or API outage

**You notice:** answers take 60-180 s and then fail; the CLI shows `claude exited 1` with
`rate_limit` / `overloaded` / `529` in stderr; or Slack users get "Sorry, I hit an error".

**Confirm:** `claude -p "say hi" --output-format json` and look at `is_error` and `result`.
If the raw CLI is failing, nothing in this repo will help; it is upstream.

**Fix:**
- Rate limit on the Claude Code subscription: wait, or switch the brain to the API backend
  (`BRAIN=api ANTHROPIC_API_KEY=...`), which has its own limits.
- Persistent 5xx: check status.anthropic.com, post in #ai-tools that the helper is degraded.
- The handler already fails safe (error message in thread, :eyes: removed), so the bot does not
  need restarting; it recovers on the next question.
- If users are hammering it, the cheapest lever is `HELPER_MODEL=claude-sonnet-5-5` (about half the
  cost per answer in the eval), then `--max-turns` in `helper/brain.py` (8 is generous; 5 is enough).

## 4. Knowledge base out of date (confidently wrong answers)

**You notice:** `feedback.jsonl` shows :-1: on a question, or someone says "the bot told me 28 days but
it's 30 now". This is the most likely failure and the one nobody will page you about.

**Confirm:** `jq -r 'select(.rating=="down") | [.question, (.sources|join(","))] | @tsv' feedback.jsonl`
and read the cited doc. The bot only knows what is in `kb/`; if the doc is stale, the answer is stale.

**Fix:**
1. Edit the markdown in `kb/`. Keep the "Last reviewed" line current; it is quoted in answers.
2. If a number changed, update the matching line in `evals/questions.yaml`.
3. `make evals`; commit `evals/last_run.md` with the change so the next person sees the scorecard moved.
4. Nothing to restart: the MCP server reads files from disk on every call.

Weekly: `jq -r .rating feedback.jsonl | sort | uniq -c`. If :-1: is above about 20% of ratings for
two weeks, stop and read every downvoted thread before touching the prompt.

## 5. Bot answers but ignores the rules (no Sources line, guesses, too long)

**Confirm:** `make evals`. The scorecard tells you which rule broke (missing fact, wrong source,
answered instead of refusing).

**Fix:** edit `SYSTEM_PROMPT` in `helper/brain.py`, re-run `make evals`, keep the new `last_run.md`.
Change one instruction at a time; the eval is 12 calls and about a dollar, so iterate freely.
