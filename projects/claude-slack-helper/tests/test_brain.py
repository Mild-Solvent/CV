"""Pure parts of helper/brain.py: source parsing, refusal rule, the claude command, cost estimate."""
import json
from types import SimpleNamespace

import helper.brain as brain
from helper.brain import Answer, _split_sources, claude_code_command


def test_split_sources_strips_the_line_and_sorts_names():
    text, sources = _split_sources("You get 28 days.\n\nSources: travel-booking.md, pto-policy.md")
    assert text == "You get 28 days."
    assert sources == ["pto-policy.md", "travel-booking.md"]


def test_split_sources_handles_none_and_bold():
    assert _split_sources("Which limit?\n*Sources:* none") == ("Which limit?", [])
    assert _split_sources("no line at all") == ("no line at all", [])


def test_refusal_rule_is_case_insensitive_and_in_system_prompt():
    assert Answer(text="I DON'T know, ask #it-help").refused
    assert not Answer(text="You get 28 days").refused
    assert brain.REFUSAL in brain.SYSTEM_PROMPT


def test_claude_command_restricts_tools_to_the_kb():
    cmd = claude_code_command("q", "/tmp/x.json")
    assert cmd[:3] == ["claude", "-p", "q"]
    assert cmd[cmd.index("--tools") + 1] == ""
    assert cmd[cmd.index("--allowedTools") + 1].split(",") == brain.MCP_TOOLS
    assert "--strict-mcp-config" in cmd and "--permission-prompts" in cmd


def test_claude_code_backend_parses_json(monkeypatch):
    fake = {"result": "28 days.\nSources: pto-policy.md", "total_cost_usd": 0.0123, "is_error": False, "num_turns": 3}

    def fake_run(cmd, **kw):
        assert "--mcp-config" in cmd
        return SimpleNamespace(returncode=0, stdout=json.dumps(fake), stderr="")

    monkeypatch.setattr(brain.subprocess, "run", fake_run)
    a = brain.answer("How many days?", backend="claude-code")
    assert (a.text, a.sources, a.cost_usd, a.cost_source) == ("28 days.", ["pto-policy.md"], 0.0123, "reported")
    assert a.raw["num_turns"] == 3


def test_api_cost_estimate_uses_price_table():
    usage = SimpleNamespace(input_tokens=1_000_000, output_tokens=0, cache_read_input_tokens=0, cache_creation_input_tokens=0)
    assert brain._estimate_cost("claude-opus-5-5", usage) == 4.0
    assert brain._estimate_cost("some-unknown-model", usage) is None
