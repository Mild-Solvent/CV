"""MCP server exposing the Orbit Research knowledge base over stdio.

Run:  python mcp_server/server.py
Claude Code loads it via --mcp-config (see helper/brain.py); any other MCP
client (Claude Desktop, the API with an MCP bridge) can use it the same way.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # allow `import kb` when run as a script
import kb  # noqa: E402
from mcp.server.mcpserver import MCPServer  # noqa: E402

server = MCPServer("orbit_kb", instructions="Internal policy docs for Orbit Research staff.")


@server.tool()
def list_docs() -> list[dict[str, str]]:
    """List every document in the knowledge base (file name and title)."""
    return kb.list_docs()


@server.tool()
def search_docs(query: str) -> list[dict[str, object]]:
    """Find the documents most relevant to a question. Returns up to 3 matches
    with a score and a snippet; call read_doc on the best one to get details."""
    return kb.search_docs(query)


@server.tool()
def read_doc(name: str) -> str:
    """Return the full markdown text of one document, e.g. read_doc('pto-policy.md')."""
    return kb.read_doc(name)


if __name__ == "__main__":
    server.run(transport="stdio")
