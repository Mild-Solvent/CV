# How companies rank and filter CVs (ATS guide)

Researched 2026-10-15. Short version: the "ranking system" is an **Applicant
Tracking System (ATS)** — Workday, Greenhouse, Lever, Taleo, iCIMS, SmartRecruiters,
Teamtailor, and in SK/CZ Profesia and Jobs.cz/LMC. It does three things to a CV:

1. **Parses** it into fields (name, contact, job titles, employers, dates, skills,
   education). If parsing fails, the recruiter sees a broken profile.
2. **Filters** with rules the recruiter sets — mostly **knockout questions** on the
   application form, not the CV itself.
3. **Searches and ranks** — the recruiter types keywords or a job title into a
   search box, and some systems add an AI "match grade" next to each candidate.

A human still makes the reject decision in almost every case. The CV's job is to
(a) parse cleanly, (b) be found by the recruiter's search, and (c) score high on the
match grade so it sits at the top of the pile.

## Fact vs myth

| Claim | Verdict |
|:--|:--|
| "75% of CVs are rejected by an ATS before a human sees them" | **Myth.** No study behind it; it is usually traced to a 2012 sales claim by Preptel, a company selling CV-optimisation, and has been repeated by blogs since. In Enhancv's 2025 interviews with 25 US recruiters on 10+ ATS platforms, 23 of 25 said their system does **not** auto-reject CVs for content or formatting. |
| "Most rejections are automatic" | **Partly true, but not because of the CV.** Rejections are automatic when you answer a **knockout question** wrong: work authorisation / visa sponsorship, location, required degree, certification, years of experience, salary. One recruiter said the visa question alone removes ~30% of tech applicants. |
| "The ATS reads and scores your CV" | **True on some systems.** Workday HiredScore grades A–D on how well the CV matches the job description. Taleo ranks by required/asset criteria. iCIMS, SmartRecruiters and LinkedIn Recruiter have "fit" scores. Greenhouse says its AI does **not** score or rank. About 44% of the recruiters surveyed had a fit score; most used it as a guide, not a gate. |
| "Fancy design gets you auto-rejected" | **Myth, but it costs you.** Nothing rejects a design. What happens is the parser mangles it: wrong job titles, missing dates, skills not extracted. Then the CV doesn't come up in keyword searches and gets a low match grade. 20% of surveyed recruiters also flagged heavily designed CVs as a negative to a human. |
| "Hidden white-text keywords beat the ATS" | **Myth and harmful.** Parsers extract white text as normal text; the recruiter sees it in the parsed profile and it reads as cheating. |
| "Apply early" | **True.** Recruiters review in order received and often stop or pause the posting once they have enough good candidates. 52% said early helps. |
| "Filters reject qualified people" | **True.** Harvard Business School / Accenture *Hidden Workers* (2021): 88% of employers said their systems screen out qualified high-skill candidates for not matching criteria exactly. |

## How the big systems actually rank

| System | What it does to your application |
|:--|:--|
| **Workday** (+ HiredScore AI) | Parses the CV into the profile (you often re-type it). HiredScore grades **A** (meets or exceeds), **B** (meets), **C** (meets some), **D** (doesn't meet the basic requirements), from the CV vs the job description. No grade if the format isn't supported. Recruiters review A first. Subject of *Mobley v. Workday* (age-bias collective action certified May 2025). |
| **Oracle Taleo** | **Disqualification questions** exit you instantly. Prescreening questions are marked *Required* or *Asset*, optionally weighted. "ACE" candidates = all Required + some Assets, and they're shown first. Everyone else sinks. |
| **Greenhouse** | No AI ranking. Recruiter-set auto-reject rules on form answers (e.g. "no" to work eligibility). Queue is reviewed in order received, filtered by referral, internal, or custom-question answers. AI only suggests keyword synonyms for recruiter search. |
| **Lever** | Search plus tags; keyword and boolean search over parsed profiles. Knockout questions on the form. |
| **iCIMS / SmartRecruiters / Eightfold** | AI "role fit" / match scores from skills and titles, shown as a ranking column. |
| **LinkedIn Recruiter / Easy Apply** | Matches on **headline, current title, skills section** and screening questions. Your LinkedIn profile is effectively a second CV. |
| **Profesia / Jobs.cz (SK/CZ)** | Structured profile fields + a closed skill taxonomy; employers filter by skill, language level and location. Spell skills the way their list does. |

## What the ranking keys on (in order of weight)

1. **Job title match.** Searches and match grades weight the title heavily. If the
   posting says "Full-Stack Developer", your most recent title should say that, not
   "Thinker · AI Wizzard".
2. **Hard skills / keywords from the job description**, spelled the same way
   (`TypeScript`, `Go`/`Golang`, `PostgreSQL`, `React`, `Docker`, `Unreal Engine 5`).
   Include both the acronym and the long form once: "Large Language Models (LLM)".
3. **Recency and duration** — skills used in your current job count more than in a
   side project. That needs **dates on every job**, `MMM YYYY – MMM YYYY` or
   `MMM YYYY – Present`.
4. **Requirements**: years of experience, degree, language level, location,
   work authorisation — mostly asked as form questions.
5. **Section headings** the parser recognises: `Summary`, `Experience`,
   `Projects`, `Skills`, `Education`, `Certifications`, `Languages`.

## Format rules that keep the parser happy

- One column, top to bottom. No tables, text boxes or sidebars for core content.
- Contact info in the body, not in the page header/footer.
- Real text, not images or canvas drawings. A selectable-text PDF or a .docx.
- Standard fonts, normal bullets (`•` or `-`), no icons in place of words.
- Reverse-chronological: newest job first.
- File name `Firstname-Lastname-CV.pdf`.
- 1–2 pages. Each bullet: action + what + result/number.

## The practical strategy

Keep **two CVs**:

- **The pixel CV** (`FINAL/index.html`) — for humans: portfolio link, emails to a
  person, game studios, the "wow" moment.
- **The ATS CV** (`FINAL/ats.html` → `FINAL/Denis-Matejcik-CV-ATS.pdf`) — for any
  "Upload your CV" form on Workday, Greenhouse, Lever, Taleo, etc.

For each application: compare the ATS CV to the job description (see
[`ats_score.py`](ats_score.py)), add the 3–5 missing keywords **that are true**,
match the headline to the posting's title, answer knockout questions honestly and
precisely, and apply within the first few days.

## EU note

Under the EU AI Act, AI used to screen or rank job candidates is **high-risk**
(Annex III). The obligations were due 2 Aug 2026; the Digital Omnibus moves them to
2 Dec 2027 (Parliament approved June 2026 — check whether it is in force). Under GDPR
Art. 22 you can ask an EU employer whether a decision about you was fully automated
and request human review.

## Sources

- Enhancv recruiter interviews (2025): https://enhancv.com/blog/does-ats-reject-resumes/
- Greenhouse, "What really happens after you apply": https://my.greenhouse.com/blogs/what-really-happens-after-you-apply-for-a-job
- Workday HiredScore grades: https://doc.workday.com/hiredscore/en-us/workday-hiredscore/recruiter-productivity-/concept--hiredscore-grades.html
- Oracle Taleo candidate prescreening: https://docs.oracle.com/en/cloud/saas/taleo-enterprise/20b/otrec/candidate-prescreening.html
- HBS/Accenture *Hidden Workers* via HR Dive: https://www.hrdive.com/news/report-applicant-tracking-systems-may-exclude-whole-segments-of-candidates/606614/
- Mobley v. Workday: https://www.hklaw.com/en/insights/publications/2025/05/federal-court-allows-collective-action-lawsuit-over-alleged
- EU AI Act Digital Omnibus timing: https://remoteworkeurope.eu/news/2026/eu-digital-omnibus-ai-employment-rules-delay-december-2027
