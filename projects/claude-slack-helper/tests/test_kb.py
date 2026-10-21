"""The MCP tools' logic (mcp_server/kb.py) and the stdio server's tool list."""
import asyncio

import kb


def test_list_docs_has_all_seven_with_titles():
    docs = kb.list_docs()
    assert len(docs) == 7
    assert {"name": "pto-policy.md", "title": "Paid time off (PTO) policy"} in docs


def test_search_ranks_the_right_doc_first():
    cases = {
        "How many days of PTO do I get?": "pto-policy.md",
        "hotel cap for a conference": "travel-booking.md",
        "my laptop was stolen": "laptop-it-setup.md",
        "need more API credits": "ai-tool-budget.md",
        "receipt for expenses": "expense-policy.md",
        "licensed dataset in Claude": "data-handling.md",
        "probation feedback": "onboarding-checklist.md",
    }
    for query, expected in cases.items():
        assert kb.search_docs(query)[0]["name"] == expected, query


def test_search_returns_snippet_and_caps_results():
    results = kb.search_docs("days")
    assert 1 <= len(results) <= 3
    assert all(r["snippet"] for r in results)
    assert kb.search_docs("the of and") == []          # only stop words


def test_read_doc_accepts_bare_name_and_blocks_path_escape():
    assert kb.read_doc("pto-policy").startswith("# Paid time off")
    assert kb.read_doc("../README.md").startswith("No doc named")
    assert "Known docs:" in kb.read_doc("nope.md")


def test_mcp_server_exposes_three_tools():
    from mcp_server import server

    names = {t.name for t in asyncio.run(server.server.list_tools())}
    assert names == {"list_docs", "search_docs", "read_doc"}
