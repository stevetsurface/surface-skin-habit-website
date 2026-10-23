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

Nine source-labelled comparison images are published from the Surface marketing PDF supplied by the website owner. Rendered clips preserve source privacy masks and session labels. The elapsed time between images was not provided; captions say so and explain differences in lighting/angle and individual outcomes. Do not retouch skin or replace images with generated results.

`skin_education.py` renders the interactive anatomy guide, relevant comparison cases, and bilingual recovery sections. `content/recovery-guides.json` contains treatment-family recovery, temporary effects, risks, preparation, and clinical references. These are patient education; the treating clinician must confirm the actual device/product, settings, personal risks, and aftercare. Avoid universal repeat intervals or claims of zero risk/downtime.

### Mobbin design references

The editorial care index and homepage use Surface's own copy and imagery, informed by Face Formula's image-led section hierarchy: https://mobbin.com/sites/sections/d7990263-c447-4583-bca4-f88350bde068 . The live preference summary adapts the appointment-context pattern studied in Selfridges: https://mobbin.com/screens/6a125d3d-8205-48df-b47b-73405156d956 . No reference screenshots are embedded in the public website. The form requests preferences; it does not present live availability or reserve a slot.
