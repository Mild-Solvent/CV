# Pixel CV — final version

One self-contained file: [`index.html`](index.html) (fonts and pixel characters are embedded — no dependencies, works offline).

## Edit the texts

Open `index.html` and search for `✏️ EDIT` — every editable spot is marked:

- your name, role line, and intro
- contact slots (email / github / base)
- each of the 4 project sections (title, chip label, description)
- education line at the bottom (kept deliberately quiet)

Keep descriptions to ~3 short sentences so everything stays on one A4 page.

## Play with it (web version)

- **GITHUB block** — pull the little lever (or click the block): it drops the next
  level for the courier (LVL 5, 6, 7 …) and the EXP bar fills up.
- **LVL 1** — click anywhere on the stage to shoot. The drone only comes down when
  you hit it — and the pilot is not happy about it.
- **LVL 2** — click the sea slug: a timing bar appears; click again when the marker
  is in the green middle and the slug rides the crab away.
- **LVL 3** — poke the agent 5× fast. (He'll fetch a new one.)
- **LVL 4** — click the bulb to make it fly off right away.
- **Bottom line** — click it to drop more dots for the sweeper.

## Export to PDF

The PDF is static — animations only live on the web version. When printing,
every scene freezes into its poster frame and the whole sheet is scaled as one
picture onto a single A4 page (same layout and line breaks as on screen).

1. Open `index.html` in Chrome/Edge (desktop)
2. `Ctrl+P` → Destination: **Save as PDF**
3. Paper size: **A4**, Margins: **None** (or Default), Scale: **100%**
4. Enable **Background graphics** ← important, otherwise colors disappear
5. Save

## Publish to GitHub Pages

A workflow is included at `.github/workflows/deploy-cv.yml`. To activate it:

1. Push this repo to GitHub
2. Repo **Settings → Pages → Source: GitHub Actions**
3. Push any change to `FINAL/` (or run the workflow manually from the Actions tab)

The site will appear at `https://<username>.github.io/<repo>/`
(likely `https://mild-solvent.github.io/CV/`).
