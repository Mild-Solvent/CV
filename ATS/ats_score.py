#!/usr/bin/env python3
"""Rough ATS check: how a CV parses and how well it matches a job description.

Mimics what Workday/HiredScore, Taleo and recruiter keyword search look at:
parseable text, contact details, standard section headings, dated jobs, the
job title, and the hard-skill keywords of the posting. It is a heuristic, not
any vendor's real algorithm.

    python3 ATS/ats_score.py FINAL/Denis-Matejcik-CV-ATS.pdf job.txt
    python3 ATS/ats_score.py FINAL/Denis-Matejcik-CV.pdf            # parse check only

CV may be .pdf (needs `pdftotext`), .html or .txt. Job description is plain text.
"""
import html
import re
import subprocess
import sys

# canonical skill -> spellings an ATS might see. Extend as needed.
SKILLS = {
    "TypeScript": ["typescript", "ts"], "JavaScript": ["javascript", "js", "ecmascript"],
    "Go": ["golang", "go"], "Python": ["python"], "C#": ["c#", "csharp", ".net", "dotnet"],
    "C++": ["c++", "cpp"], "Java": ["java"], "Kotlin": ["kotlin"], "Rust": ["rust"],
    "PHP": ["php"], "SQL": ["sql"], "PowerShell": ["powershell"], "Lua": ["lua"],
    "React": ["react", "reactjs", "react.js"], "React Native": ["react native"],
    "Next.js": ["next.js", "nextjs"], "Vue": ["vue", "vue.js", "vuejs"], "Nuxt": ["nuxt", "nuxt.js"],
    "Angular": ["angular"], "Node.js": ["node.js", "nodejs", "node"], "GraphQL": ["graphql"],
    "REST": ["rest", "restful", "rest api", "rest apis"], "gRPC": ["grpc"],
    "PostgreSQL": ["postgresql", "postgres"], "MySQL": ["mysql"], "MongoDB": ["mongodb", "mongo"],
    "Redis": ["redis"], "Supabase": ["supabase"], "Firebase": ["firebase"],
    "Docker": ["docker"], "Kubernetes": ["kubernetes", "k8s"], "Terraform": ["terraform"],
    "AWS": ["aws", "amazon web services"], "GCP": ["gcp", "google cloud"], "Azure": ["azure"],
    "Linux": ["linux"], "CI/CD": ["ci/cd", "ci", "github actions", "gitlab ci"], "Git": ["git"],
    "Android": ["android"], "iOS": ["ios"], "WebRTC": ["webrtc"],
    "LLM": ["llm", "llms", "large language model", "large language models"],
    "AI agents": ["ai agent", "ai agents", "agentic", "agent workflows"],
    "MCP": ["mcp", "model context protocol"], "RAG": ["rag", "retrieval augmented"],
    "OpenAI API": ["openai"], "LangChain": ["langchain"], "Machine learning": ["machine learning", "ml"],
    "Unreal Engine": ["unreal", "unreal engine", "ue5", "ue4"], "Unity": ["unity"],
    "Blueprints": ["blueprints", "blueprint"], "Godot": ["godot"],
    "ROS": ["ros", "ros2"], "PX4": ["px4"], "ArduPilot": ["ardupilot"], "MAVLink": ["mavlink"],
    "Computer vision": ["computer vision", "opencv"], "Embedded": ["embedded", "firmware"],
    "Microservices": ["microservices", "microservice"], "Testing": ["unit testing", "tdd", "jest", "pytest"],
    "Agile": ["agile", "scrum"], "SEO": ["seo"],
}
HEADINGS = ["summary|profile|about", "experience|employment|work history",
            "skills|technical skills", "education", "projects", "languages", "certifications"]
DATE = re.compile(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{4}|\b(19|20)\d{2}\s*[–-]\s*(present|now|current|(19|20)\d{2})", re.I)


def read(path):
    if path.endswith(".pdf"):
        return subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True, check=True).stdout
    text = open(path, encoding="utf-8").read()
    if path.endswith((".html", ".htm")):
        text = re.sub(r"(?is)<(script|style).*?</\1>|<!--.*?-->", " ", text)
        text = html.unescape(re.sub(r"<[^>]+>", " ", text))
    return text


def has(term, text):
    return re.search(r"(?<![a-z0-9+#])" + re.escape(term) + r"(?![a-z0-9+#])", text) is not None


def skills_in(text):
    t = text.lower()
    return {k for k, alts in SKILLS.items() if any(has(a, t) for a in alts)}


def parse_report(cv):
    low = cv.lower()
    words = len(cv.split())
    checks = [
        ("text extractable (>250 words)", words > 250, f"{words} words"),
        ("email found", bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", cv)), ""),
        ("phone found", bool(re.search(r"\+?\d[\d \-]{8,}\d", cv)), "add one in the copy you upload"),
        ("linkedin found", "linkedin" in low, ""),
    ]
    for h in HEADINGS:
        checks.append((f"heading: {h.split('|')[0]}", bool(re.search(r"(?im)^\s*(" + h + r")\s*$", cv)), ""))
    dates = len(DATE.findall(cv))
    checks.append(("dated jobs (>=2 date ranges)", dates >= 2, f"{dates} found"))
    return checks


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cv = read(sys.argv[1])
    print(f"== Parse check: {sys.argv[1]}")
    checks = parse_report(cv)
    for name, ok, note in checks:
        print(f"  [{'x' if ok else ' '}] {name}" + (f"  ({note})" if note else ""))
    parse_score = round(100 * sum(ok for _, ok, _ in checks) / len(checks))
    print(f"  parse score: {parse_score}/100")
    if len(sys.argv) < 3:
        return
    jd = read(sys.argv[2])
    want, have = skills_in(jd), skills_in(cv)
    hit, miss = sorted(want & have), sorted(want - have)
    kw = round(100 * len(hit) / len(want)) if want else 100
    first = next((line.strip() for line in jd.splitlines() if line.strip()), "")
    title_words = [w for w in re.findall(r"[a-z]+", first.lower()) if len(w) > 2 and w not in {"the", "and", "for", "with", "remote", "senior", "junior"}]
    title_hit = sum(w in cv.lower()[:600] for w in title_words)
    title = round(100 * title_hit / len(title_words)) if title_words else 100
    total = round(0.6 * kw + 0.25 * title + 0.15 * parse_score)
    grade = "A" if total >= 85 else "B" if total >= 70 else "C" if total >= 50 else "D"
    print(f"\n== Match vs {sys.argv[2]}")
    print(f"  job title (first line): {first!r} -> {title}% of its words near the top of the CV")
    print(f"  keywords: {len(hit)}/{len(want)} ({kw}%)")
    print(f"    matched: {', '.join(hit) or '-'}")
    print(f"    missing: {', '.join(miss) or '-'}")
    print(f"\n  overall ~{total}/100, grade {grade}  (A meets/exceeds, B meets, C some, D doesn't — HiredScore-style)")
    print("  Only add a missing keyword if it is true. Mirror the posting's spelling.")


if __name__ == "__main__":
    main()
