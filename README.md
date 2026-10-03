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
- MIRA: NeurIPS 2026 Poster, confirmed by the author in October 2026.
- SearchWeave: ongoing work, with a short public description and “Work in progress” status. No result numbers, conference acceptance, training details, or unverified author list are added.
- Draft PDFs and acceptance emails are not included in this repository. All four research thumbnails are original illustrative SVG schematics, not experimental figures. Legacy PNG paths contain the same schematics for compatibility.
- The public CV omits the phone number and fixes the original PDF's incorrect email hyperlink. It is generated from professional information in the supplied CV.
- `Lora` and `Poppins` are loaded from Google Fonts, with system font fallbacks.

The source CV and papers remain unchanged.
