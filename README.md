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

## Education, proof, and the consultation journey

`site_features.py` adds the 26 treatment guides, skin-layer illustrations, brand wall, Surface story, attributed customer-story summaries, visit guidance, and the expanded booking form. `content/catalog.json` holds the content and original testimonial links.

The form supports clinic, concern, first/review/return visit, and date/time preferences, plus concern deep links such as `?concern=TONE&visit=followup`. It opens an appointment request on WhatsApp; it does not reserve a calendar slot or send automated reminders.

Run `node tests/booking.cjs` to verify handoff context and request wording.

### Before-and-after assets

No result photos are currently published. To add a real case to `results.items`, supply `publish: true`, `consent`, `doctor_approved: true`, a `concern` code, local `before` and `after` image paths, `treatment`, `timeframe`, `caption`, and `caption_en`. The results renderer shows only complete cases with both images present. Confirm comparable lighting/angles and actual timing. Never substitute another clinic's images or generated pictures as Surface results.
