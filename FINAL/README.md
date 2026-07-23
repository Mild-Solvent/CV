# Pixel CV — final version

One self-contained file: [`index.html`](index.html) (fonts and pixel characters are embedded — no dependencies, works offline).

## Edit the texts

Open `index.html` and search for `✏️ EDIT` — every editable spot is marked:

- your name, role line, and intro
- contact slots (email / github / base)
- each of the 4 project sections (title, chip label, description)

Keep descriptions to ~3 short sentences so everything stays on one A4 page.

## Export to PDF

The PDF is static — animations only live on the web version. When printing,
the characters automatically freeze into a clean standing pose.

1. Open `index.html` in Chrome/Edge
2. `Ctrl+P` → Destination: **Save as PDF**
3. Paper size: **A4**, Margins: **None** (or Default)
4. Enable **Background graphics** ← important, otherwise colors disappear
5. Save

## Publish to GitHub Pages

A workflow is included at `.github/workflows/deploy-cv.yml`. To activate it:

1. Push this repo to GitHub
2. Repo **Settings → Pages → Source: GitHub Actions**
3. Push any change to `FINAL/` (or run the workflow manually from the Actions tab)

The site will appear at `https://<username>.github.io/<repo>/`
(likely `https://mild-solvent.github.io/CV/`).
