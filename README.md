# Zhihan Yin — Academic homepage

Static academic website for https://hans-m-yin.github.io.

## Edit content

Personal information, publications, experience, and awards are in `data/site.json`.

After editing, run:

```bash
python3 scripts/build.py
```

To regenerate the public CV (requires `reportlab`):

```bash
python3 scripts/make_cv.py
```

Add a portrait to `assets/images/portrait.jpg`, set `portrait` to
`/assets/images/portrait.jpg` in `data/site.json`, and rebuild.

Preview locally:

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

## GitHub Pages

The repository name is `Hans-M-Yin.github.io`. In **Settings → Pages**, choose
**Deploy from a branch → main → /(root)** and save. No Ruby, Jekyll, Node, or
server runtime is required to publish the generated files.

## Content notes

- Layout inspired by https://jiaxuanzou0714.github.io/ (an al-folio-style academic website). This implementation uses original HTML, CSS, and JavaScript.
- FREAK: ICLR 2026, confirmed by the supplied acceptance notice and the official repository. Paper: https://arxiv.org/abs/2603.19765.
- Veto: ACM Multimedia 2026, confirmed by the supplied notice and the conference technical programme. Author spelling follows the programme.
- MIRA: status is “NeurIPS 2026 submission”, as listed in the supplied CV. No acceptance claim is made.
- SearchWeave: ongoing work, shown first. No result numbers, conference acceptance, or unverified author list is added. The draft has an outdated ICLR 2025 template header; the website uses “Work in progress”.
- Draft PDFs and acceptance emails are not included in this repository. SearchWeave and MIRA figures are cropped from the user-supplied PDFs. FREAK and Veto thumbnails are illustrative research schematics, not experimental figures.
- The public CV omits the phone number and fixes the original PDF's incorrect email hyperlink. It is generated from professional information in the supplied CV.
- `Lora` and `Poppins` are loaded from Google Fonts, with system font fallbacks.

The source CV and papers remain unchanged.
