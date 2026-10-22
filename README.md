# Surface Skin Habit

Complete bilingual static website for GitHub Pages. Indonesian at the root; English under `en/`.

## Rebuild

```sh
python3 build.py
python3 check.py
node --check assets/redesign.js
node --check assets/analisis.js
```

Commit the generated HTML and assets with source changes. GitHub Pages serves the main branch root. The original HTML routes and language pairs are preserved.

Content and prices: `content/catalog.json`. Shared templates: `build.py`. Specialist reference content and assessment data: `content/legacy/`. Shared styles: `assets/redesign.css`, `assets/full-site.css`, and `assets/typography.css`.

Gotham is the brand font. The source contains no licensed Gotham webfonts. Local Gotham is used where available, with Montserrat as the temporary fallback. Add licensed `Gotham-Book.woff2`, `Gotham-Medium.woff2`, and `Gotham-Bold.woff2` under `assets/fonts/`, then rebuild.

The assessment runs locally in the browser; WhatsApp sharing happens only when the visitor chooses it. Clinic selection is remembered in local storage. No patient results or testimonials have been fabricated.

Production origin: https://stevetsurface.github.io/surface-skin-habit-website
