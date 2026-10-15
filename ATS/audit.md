# ATS audit of the current CV — 2026-10-15

Audited `FINAL/Denis-Matejcik-CV.pdf` (the 2-page pixel CV served on Pages) by
extracting its text the way a parser does (`pdftotext`) and running
[`ats_score.py`](ats_score.py).

## Verdict

The pixel CV is great for a human and weak for an ATS. Nothing will auto-reject it,
but a parser gets a profile with **no job titles, no employer dates, no recognised
sections and no skills list**, so it ranks low in recruiter searches and AI match
grades. Fix: keep it, and add a plain ATS twin for upload forms — now in
[`FINAL/ats.html`](../FINAL/ats.html) → [`FINAL/Denis-Matejcik-CV-ATS.pdf`](../FINAL/Denis-Matejcik-CV-ATS.pdf).

| Check | Pixel CV | ATS CV |
|:--|:--|:--|
| Parse score (contact, 7 headings, dates) | **17/100** | **92/100** (no phone, on purpose) |
| Sample job: *Software Engineer – Backend Services* (MPG / Keywords Studios, from `job-search/jobs`) | **26/100, grade D** · 4/14 keywords | **63/100, grade C** · 7/14 keywords |

Same facts, different packaging. The remaining gap on that job (AWS, Azure, Java,
Kotlin, Kubernetes, Terraform, C++) is real experience he doesn't list, not
formatting — don't add those unless they are true.

## What a parser sees in the pixel CV

1. **The first lines are game UI**: `PLAYER 1 · EXP · WORLD 2026 · Thinker · AI
   Wizzard`. Parsers often take the top line as the name/headline, so the headline
   may be stored as "Thinker AI Wizzard".
2. **No job titles.** Entries are `GAS.GREEN DELIVERY STARTUP`, `AI AGENTS B2B
   STARTUP`. The title field is the most heavily weighted in search and match
   grading; it comes out empty.
3. **No employer for the AI job.** teamday.ai isn't named anywhere.
4. **No date ranges.** Years appear as `NOW`, `2026`, `ALWAYS`. Parsers can't compute
   experience length or recency, so "3+ years TypeScript" filters miss him.
5. **No standard headings.** `THE CHRONICLE`, `QUEST LOG`, `LVL 1–4`, `EDU` aren't
   recognised as Summary / Experience / Projects / Education.
6. **No skills section.** Skills only appear inside the small stack lines.
   React, Node.js, Python, Firebase and GCP (all on his Profesia
   profile) don't appear in the PDF at all.
7. **The drop-cap "I" disappears** — the text starts `’m a passionate developer`.
   The hidden real "I" (`.dc-hide`, clipped to 1px) is dropped by Chrome's PDF
   export.
8. **No LinkedIn, no phone, no languages, no A1/A3 certification** — all things
   forms and filters ask for.
9. **Page 2 repeats page 1** in a shorter form, which doubles some text and
   confuses entry boundaries.

## What was changed (safe, nothing removed)

- Added `FINAL/ats.html`: one column, real text, standard headings, job titles
  from `job-search/profile-kit.md`, `MMM YYYY – MMM YYYY` dates, a grouped skills
  section, languages, certification, LinkedIn. Deployed with the site at
  `https://mild-solvent.github.io/CV/ats.html`.
- Added `FINAL/Denis-Matejcik-CV-ATS.pdf` rendered from it (headless Chromium, A4).
- The pixel CV is untouched.

## Still to decide / do by hand

- **Phone number** is left out because the site is public. Add it to the copy you
  upload (`+421 …`).
- **"EU citizen, no sponsorship needed"** is in the contact line because visa
  knockout questions remove a big share of applicants. Confirm it's right.
- **Study years** for Middlesex and SPŠ are unknown; some forms require them.
- **Title per application**: change the headline line to the posting's exact title
  (e.g. "Backend Software Engineer", "Gameplay/Tools Programmer", "AI Engineer").
- Optional: fix the drop-cap export by giving `.dc-hide` `color:transparent`
  instead of clipping it, then re-export the pixel PDF.
