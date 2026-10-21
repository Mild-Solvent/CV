"""The "brain": turns a staff question into an answer grounded in kb/.

Two interchangeable backends, chosen with BRAIN=claude-code|api:

* claude-code (default): runs `claude -p` headless with the MCP server from
  mcp_server/ as its only tools. Same runtime, skills and prompts that staff
  use interactively; nothing to maintain twice.
* api: the Anthropic Python SDK Messages API with a hand-written tool loop,
  calling the same functions in mcp_server/kb.py directly. For teams that
  have an API key but no Claude Code licence. Untested in the environment
  this was built in (no ANTHROPIC_API_KEY there) - see README.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "mcp_server"))
import kb  # noqa: E402

MCP_TOOLS = ["mcp__orbit_kb__search_docs", "mcp__orbit_kb__read_doc", "mcp__orbit_kb__list_docs"]
DEFAULT_MODEL = os.environ.get("HELPER_MODEL", "claude-opus-5-5")
CLAUDE_TIMEOUT_S = int(os.environ.get("HELPER_TIMEOUT_S", "180"))
REFUSAL = "I don't know, ask #it-help"

SYSTEM_PROMPT = f"""You are the Orbit Research staff helper in Slack. You answer questions about
internal policy using ONLY the knowledge base exposed by the orbit_kb tools.

How to work:
1. Call search_docs with the key words of the question, then read_doc on the best match
   (read a second doc if the first one does not settle it). Never answer from memory.
2. Answer in 2-5 short sentences with the specific numbers, limits or steps from the doc.
   Plain English, no preamble, no headings. Slack-style bold with *asterisks* is fine.
3. If the knowledge base does not cover the question, reply with exactly:
   "{REFUSAL}" and one sentence on what you did find, if anything. Never guess.
4. If the question is genuinely ambiguous (it could refer to two different policies,
   e.g. "what is the limit?"), do not guess: ask ONE short clarifying question that names
   the options you found.
5. Finish with a final line in exactly this form, listing the file names you used:
   Sources: pto-policy.md, travel-booking.md
   Use "Sources: none" when you refused or asked a clarifying question.
"""

PRICE_PER_MTOK = {  # USD, input / output / cache read / cache write (5m); for estimates only
    "claude-opus-5-5": (4.00, 20.00, 0.20, 5.00),
    "claude-sonnet-5-5": (2.00, 10.00, 0.20, 2.50),
    "claude-haiku-5-5": (0.10, 0.50, 0.01, 0.125),
}


@dataclass
class Answer:
    text: str
    sources: list[str] = field(default_factory=list)
    cost_usd: float | None = None
    cost_source: str = "unknown"   # "reported" | "estimate" | "unknown"
    backend: str = ""
    raw: dict = field(default_factory=dict)

    @property
    def refused(self) -> bool:
        return "i don't know" in self.text.lower()


def _build_prompt(question: str, thread_context: list[str] | None) -> str:
    if not thread_context:
        return question
    history = "\n".join(f"- {m}" for m in thread_context[-8:])
    return f"Earlier messages in this Slack thread:\n{history}\n\nNew question: {question}"


def _split_sources(text: str) -> tuple[str, list[str]]:
    """Pull the trailing 'Sources: a.md, b.md' line out of the model's reply."""
    m = re.search(r"^\s*\*?Sources?:\*?\s*(.*?)\s*$", text, re.IGNORECASE | re.MULTILINE)
    if not m:
        return text.strip(), []
    body = (text[: m.start()] + text[m.end():]).strip()
    names = re.findall(r"[\w.-]+\.md", m.group(1))
    return body, sorted(set(names))


def answer(question: str, thread_context: list[str] | None = None, backend: str | None = None) -> Answer:
    backend = backend or os.environ.get("BRAIN") or ("api" if os.environ.get("ANTHROPIC_API_KEY") else "claude-code")
    if backend == "api":
        return _answer_api(_build_prompt(question, thread_context))
    if backend == "claude-code":
        return _answer_claude_code(_build_prompt(question, thread_context))
    raise ValueError(f"BRAIN must be 'claude-code' or 'api', not {backend!r}")


# --- backend 1: Claude Code headless -----------------------------------------------------

def _mcp_config() -> str:
    cfg = {"mcpServers": {"orbit_kb": {"command": sys.executable, "args": [str(ROOT / "mcp_server" / "server.py")]}}}
    f = tempfile.NamedTemporaryFile("w", suffix=".json", prefix="orbit-mcp-", delete=False)
    json.dump(cfg, f)
    f.close()
    return f.name


def claude_code_command(prompt: str, mcp_config_path: str) -> list[str]:
    """The exact `claude -p` invocation, kept separate so tests and the RUNBOOK can show it."""
    return [
        "claude", "-p", prompt,
        "--model", DEFAULT_MODEL,
        "--system-prompt", SYSTEM_PROMPT,
        "--mcp-config", mcp_config_path, "--strict-mcp-config",
        "--tools", "",                              # no Bash/Edit/Read: the KB is the only tool
        "--allowedTools", ",".join(MCP_TOOLS),
        "--permission-prompts", "none",             # anything not allowed above is denied, never prompted
        "--max-turns", "8",
        "--output-format", "json",
    ]


def _answer_claude_code(prompt: str) -> Answer:
    cfg = _mcp_config()
    try:
        proc = subprocess.run(claude_code_command(prompt, cfg), capture_output=True, text=True,
                              timeout=CLAUDE_TIMEOUT_S, stdin=subprocess.DEVNULL)
    finally:
        os.unlink(cfg)
    if proc.returncode != 0 and not proc.stdout.strip():
        raise RuntimeError(f"claude exited {proc.returncode}: {proc.stderr.strip()[:500]}")
    data = json.loads(proc.stdout)
    if data.get("is_error"):
        raise RuntimeError(f"claude reported an error: {data.get('result', '')[:500]}")
    text, sources = _split_sources(data.get("result", ""))
    cost = data.get("total_cost_usd")
    return Answer(text=text, sources=sources, cost_usd=cost,
                  cost_source="reported" if cost is not None else "unknown",
                  backend="claude-code",
                  raw={k: data.get(k) for k in ("num_turns", "duration_ms", "usage", "modelUsage", "session_id")})


# --- backend 2: Anthropic Messages API with tool use ------------------------------------

API_TOOLS = [
    {"name": "list_docs", "description": "List every document in the knowledge base (file name and title).",
     "input_schema": {"type": "object", "properties": {}, "additionalProperties": False}},
    {"name": "search_docs", "description": "Find the documents most relevant to a question (up to 3, with snippets).",
     "input_schema": {"type": "object", "properties": {"query": {"type": "string"}},
                      "required": ["query"], "additionalProperties": False}},
    {"name": "read_doc", "description": "Return the full markdown text of one document, e.g. 'pto-policy.md'.",
     "input_schema": {"type": "object", "properties": {"name": {"type": "string"}},
                      "required": ["name"], "additionalProperties": False}},
]
_API_IMPL = {"list_docs": kb.list_docs, "search_docs": kb.search_docs, "read_doc": kb.read_doc}


def _estimate_cost(model: str, usage) -> float | None:
    prices = PRICE_PER_MTOK.get(model)
    if not prices:
        return None
    inp, out, cr, cw = prices
    return (usage.input_tokens * inp + usage.output_tokens * out
            + (usage.cache_read_input_tokens or 0) * cr
            + (usage.cache_creation_input_tokens or 0) * cw) / 1_000_000


def _answer_api(prompt: str) -> Answer:
    import anthropic  # imported here so the claude-code path has no SDK dependency at runtime

    client = anthropic.Anthropic()
    messages: list[dict] = [{"role": "user", "content": prompt}]
    cost = 0.0
    turns = 0
    while True:
        response = client.messages.create(
            model=DEFAULT_MODEL, max_tokens=4096, system=SYSTEM_PROMPT,
            tools=API_TOOLS, messages=messages,
        )
        turns += 1
        cost += _estimate_cost(DEFAULT_MODEL, response.usage) or 0.0
        if response.stop_reason != "tool_use" or turns >= 8:
            break
        messages.append({"role": "assistant", "content": response.content})
        results = []
        for block in response.content:
            if block.type == "tool_use":
                out = _API_IMPL[block.name](**block.input)
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": out if isinstance(out, str) else json.dumps(out)})
        messages.append({"role": "user", "content": results})
    if response.stop_reason == "refusal":
        return Answer(text=REFUSAL + " (the model declined this request).", backend="api",
                      cost_usd=cost, cost_source="estimate")
    final = "".join(b.text for b in response.content if b.type == "text")
    text, sources = _split_sources(final)
    return Answer(text=text, sources=sources, cost_usd=cost, cost_source="estimate", backend="api",
                  raw={"num_turns": turns, "stop_reason": response.stop_reason})
