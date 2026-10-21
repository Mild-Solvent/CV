"""Knowledge-base access shared by the MCP server and the API brain.

Plain functions over the markdown files in kb/. No index, no embeddings:
the KB is small enough that keyword scoring over ~2,000 words is instant
and easy to reason about when an answer looks wrong.
"""
from __future__ import annotations

import re
from pathlib import Path

KB_DIR = Path(__file__).resolve().parent.parent / "kb"
STOP = {"the", "a", "an", "of", "to", "in", "for", "and", "or", "is", "are", "do",
        "i", "my", "we", "how", "what", "when", "can", "get", "does", "much", "many"}


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]


def _title(body: str, name: str) -> str:
    first = body.lstrip().splitlines()[0] if body.strip() else name
    return first.lstrip("# ").strip() or name


def list_docs() -> list[dict[str, str]]:
    """Return every doc as {"name": ..., "title": ...}, sorted by name."""
    out = []
    for path in sorted(KB_DIR.glob("*.md")):
        out.append({"name": path.name, "title": _title(path.read_text(), path.name)})
    return out


def read_doc(name: str) -> str:
    """Return the full text of one doc. Accepts 'pto-policy' or 'pto-policy.md'."""
    name = name.strip()
    if not name.endswith(".md"):
        name += ".md"
    path = KB_DIR / Path(name).name          # Path(...).name blocks ../ escapes
    if not path.is_file():
        known = ", ".join(d["name"] for d in list_docs())
        return f"No doc named {name!r}. Known docs: {known}"
    return path.read_text()


def search_docs(query: str, limit: int = 3) -> list[dict[str, object]]:
    """Rank docs by keyword overlap; return name, title, score and best line."""
    terms = _tokens(query)
    if not terms:
        return []
    results = []
    for path in KB_DIR.glob("*.md"):
        body = path.read_text()
        words = _tokens(body)
        title_words = _tokens(_title(body, path.name))
        score = 0.0
        for term in terms:
            stem = term[:5] if len(term) >= 5 else term  # "days" ~ "day", "expenses" ~ "expense"
            hits = sum(1 for w in words if w == term or (len(stem) >= 4 and w.startswith(stem)))
            score += min(hits, 5)                        # cap so one repeated word can't dominate
            if any(w == term or w.startswith(stem) for w in title_words):
                score += 4
        if score <= 0:
            continue
        lines = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.startswith("#")]
        best = max(lines, key=lambda ln: sum(t in ln.lower() for t in terms), default="")
        results.append({"name": path.name, "title": _title(body, path.name),
                        "score": round(score, 1), "snippet": best[:200]})
    results.sort(key=lambda r: (-r["score"], r["name"]))  # type: ignore[operator]
    return results[:limit]
