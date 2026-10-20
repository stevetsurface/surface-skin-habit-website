# Surface Skin Habit — website

Static, search-readable public site in Bahasa Indonesia and English. Eighteen pages per language, one catalog, no framework.

```
website/
  catalog.json      ← the only file you edit (prices, clinics, doctors, FAQ, WhatsApp number)
  build.py          ← turns catalog.json into the HTML pages
  index.html        ← Beranda (built)
  menu.html         ← Menu & Harga (built)
  dokter.html       ← Dokter (built)
  klinik.html       ← Klinik (built)
  analisis.html     ← Analisis Kondisi Kulit, the 13-question Smart Skin Assessment (built)
  edukasi.html      ← Edukasi, the device and procedure explainers (built)
  edukasi-*.html    ← one page per device or procedure, 11 of them (built)
  edukasi-treatment.html, edukasi-brand.html, edukasi-kombinasi.html, edukasi-waktu.html ← treatments, brands, combinations, intervals (built)
  404.html          ← catch-all, needs one line of host config (see below)
  jerawat.html, cerah.html, kencang.html ← the three concern streams (built); en/acne.html, en/brightening.html, en/firming.html in English
  en/               ← every page again in English (built); each links to its twin with hreflang
  sitemap.xml, robots.txt (built)
  assets/style.css, site.js, analisis.js, scan-adapter.js, mark.svg, favicon.svg
```

## Two languages

Indonesian is the default (site root, `x-default`). English lives under `/en/`. Every page carries `hreflang` links to its twin and the header has an EN / ID switch that keeps you on the same page.

- Catalog text: each Indonesian field has an English twin with the `_en` suffix (`intro` / `intro_en`, `desc` / `desc_en`, `q` / `q_en`, …). If the `_en` field is missing the Indonesian text is used, so a half-translated catalog still builds.
- Interface text (buttons, headings, WhatsApp message templates, the assessment's labels): the `UI` dictionary at the top of `build.py`, one block per language.
- WhatsApp messages are prefilled in the page's language. CS replies in whichever language the customer wrote in.

## Updating prices, doctors, clinics

1. Edit `catalog.json` (both the Indonesian field and its `_en` twin when the text changes).
2. Run:

```bash
python3 build.py
```

3. Upload the whole `website/` folder (minus `build.py` and `catalog.json` if you prefer) to the host.

Never hand-edit the `.html` files; the next build overwrites them.

## Why it is built this way

- **Findability.** Every page is plain HTML with the menu, prices, doctors and addresses in the markup, plus JSON-LD (`MedicalClinic`, `Physician`, `OfferCatalog`, `FAQPage`). Google can read it; the previous SPA shell could not be indexed.
- **Price anchoring.** Three concerns (Clear / Glow / Lift), three offers each from gentlest to most intensive, published with single, 3x and 6x prices. There are no level labels: the 3×3 level matrix from the September drafts was dropped; the doctor recommends a treatment, the customer picks how to buy it. No discount percentages are shown anywhere, per the Permenkes 1787/2010 note in the menu rules.
- **WhatsApp as the only booking lane.** Every CTA is a `wa.me` link with a prefilled message naming the offer. `site.js` remembers the clinic a visitor picked and adds it to later messages. The site works fully with JavaScript off.
- **One catalog, one render.** `catalog.json` is the public render of the catalog described in `SSH_Three_Flows_Menu_CRM_Web.md`. When the transactional catalog sheet exists, this file should be generated from it.

## Education (Edukasi)

`catalog.json › education` holds eleven devices and procedures, each with: brand, device type, a
one-sentence lay explanation, two paragraphs of mechanism, what it is used for, session length,
interval, downtime, what it feels like, who performs it, which clinics have it, a Fitzpatrick
safety row, who should wait, and aftercare. Plus a ten-term glossary.

The source is `SSH_Treatment_Device_Map.html` (June 2026) for device, mechanism, conditions,
clinic availability and the Fitzpatrick matrix, and `SSH_MASTER_Menu_2026.xlsx` (MENU, PROTOKOL
and MASA BERLAKU sheets) for durations and intervals. That device map is marked internal: its
sales scripts, upsell rules, promo codes, revenue figures and competitor talk track are
deliberately **not** in the catalog and must not be added.

**The clinical content needs a doctor's sign-off before this goes live.** In particular the
Fitzpatrick rows: the Biaxis page shows all three bands as a primary indication, which is true of
its 1064 nm mode and is the point of the device for Indonesian skin, with the 532 nm caveat in the
note underneath. A doctor should confirm that reading, and every contraindication list, before
publish.

## Education, part two: treatments, brands, combinations, timing (added 20 Oct 2026)

Four more pages hang off the Edukasi hub, all built from `catalog.json › education`:

- `treatments` (24 rows, six families): who performs it, duration, interval, what it is for, the device page it links to, and the single list price from the Master Menu DAFTAR HARGA sheet. Items without a settled price (skin boosters) show "at consultation".
- `brands` (17): maker, type, what it does, which treatments use it.
- `combinations`: five rules of combining, six chair sequences with minutes and a week-by-week results timeline (from the Master Menu PROTOKOL sheet, generalised to the current offers), and the pairs that do not share a visit.
- `timing`: interval table by treatment type, programme length and validity (MASA BERLAKU sheet), waiting rules (isotretinoin, sun, pregnancy, other clinics), and the rebooking windows from the CS handbook.

Sequence minutes and timelines are the September proposals marked "until the Medical Lead signs them off" in the source sheet. **They need the same doctor sign-off as the device pages before go-live.**

## Brand list source (20 Oct 2026)

The brands page is reconciled against the clinic's 2026 consumables register, which is the real product list. It added Prostrolane Blanc-B (Caregen), Juvelook (VAIM), ASCE+ exosome (ExoCoBio), Vitaran, XelaRederm (Hyalual), Innoaesthetics, MCCM, Kalbe/Dermaqual, PRP kits, DermalInfusion serums and AQ Recovery Serum, and removed Thesera, Dermashine and Athena, which are not in the 2026 cost. Supplier names are deliberately not published.

**Not on the website, on purpose:** the pharmacy's prescription products and the weight programme's medicines are prescription-only. Obat keras may not be advertised to the public in Indonesia, so the site says only that doctor-prescribed products are available at the clinic pharmacy. Costs and margins are never copied into `catalog.json`.

## Five funnels (20 Oct 2026, later)

The concerns and streams are now the five-stage ladder from the master menu's journey sheet, in life-stage order: Clear (jerawat / clear), Tone (cerah / tone), Texture (tekstur / texture, including the sensitive-skin and barrier track), Tighten (kencang / tighten), Enhance (penyempurnaan / enhance). Offers are combinations named on the master menu with its 1x/3x/6x prices; offers without a settled package price show "at consultation". The home page shows a funnel strip and five cards; every programme page carries the strip. The assessment routes to all five.

## Blog, CS explainer, SEO map, social proof (20 Oct 2026, later)

- `posts` in catalog.json render `blog.html` and one `blog-<slug>.html` per post per language, with Article JSON-LD and a CTA to the matching funnel. Four cornerstone posts cover the keywords the July brief said are winnable: harga HIFU Jakarta, Rejuran vs Profhilo vs Nucleofill, bekas jerawat bopeng, klinik kecantikan Jakarta Selatan. Add a post by adding an object to `posts`.
- `cs.html` (noindex) is the customer-service explainer: fourteen common questions, each with the short answer, the page to send, and the WhatsApp template from the CS handbook, with copy buttons. `seo.html` (noindex) is the keyword → page map with the content rules.
- Instagram: set `social.instagram.posts` to public post URLs and the home page embeds them with Instagram's official script; empty shows placeholder tiles. The handle `surfaceskinhabit` came from a third-party listing: confirm it.
- Google: each clinic links to its Maps listing for reviews; fill `clinics[].google_place_id` to enable the "write a review" link. Claim all four listings in Google Business Profile.
- Design placeholders: `site.show_placeholders: true` renders dashed boxes where the team should drop photos (hero, per funnel, per clinic, doctors, review widget, Instagram). Set it to `false` for launch.
- Type: the font stack is Gotham with Montserrat as fallback. Gotham is a licensed Hoefler font; put licensed woff2 files in `assets/fonts/` and add `@font-face` rules to use it for real.

## Streams and the USP (20 Oct 2026)

`catalog.json › streams` holds one landing page per concern (CLEAR → jerawat / acne, GLOW → cerah / brightening, LIFT → kencang / firming). Each has: a headline in customer language, "this is for you if", a four-step journey with timing (free doctor consult, start offer, 3–6 session programme with week-4 and week-8 checkpoints, week-12 doctor review then hold), what we promise, what we do not promise, the three offers with prices, the device logos used, the USP block, doctors, and three concern-specific FAQs. The home-page concern cards, the menu sections and the footer link to them. Stream filenames differ per language; `alt_path()` in build.py maps them for hreflang, the language switch and the sitemap.

`catalog.json › usp` is the positioning block shown on the home page and every stream: "Bukan sekali treatment. Kebiasaan kulit." with five points (doctor decides; dated plan with week-12 review; open prices at four clinics; we name our devices; one record, four clinics). It comes from the July 2026 competitive brief: every competitor sells treatments, none sells a programme, and "the one-off treatment that leads nowhere" is the category villain no one else has claimed. The Oct 2026 OORA battle card could not be decoded (ReportLab PDF with subset fonts), so it is not reflected; read it and adjust the USP if OORA claims the same ground.

Copy rule the lint enforces: never write whitening or skin-lightening words, even to deny them ("tidak ada klaim memutihkan" fails the build). Say "mengubah warna kulit" instead.

## Brands page: origin, clearances, logos (20 Oct 2026)

Each brand in `catalog.json › education.brands` now carries `origin`, `site` (official website, only where the domain was checked), `regulatory` (a list of verified clearances with a source link), `kemenkes_akl` (blank; fill from the device's izin edar document and it renders as a chip), and `logo` (a filename under `assets/brands/`). The page also shows a device × clinic matrix from `education.devices[].clinics`, and the home page carries a brand strip.

Verified so far: Celluma FDA-cleared (BioPhotas, USA); Pollogen Legend+ FDA 510(k) K171359 (TriPollar applicators, 2017); Liftera Korea MFDS approval (2016); BiAxis made by HLS Hypertech Laser Systems, Lübeck, Germany (ISO 13485 per a business directory). Not verifiable from public sources: Cellec V, Aquapure, Mediderma Nanopore, LHALA/H2MEDI. **Do not add a clearance without a source URL in the entry.** The Indonesian registration numbers (AKL) are in the clinic's own izin edar files, not online; that is the one every Indonesian customer can ask about, so it is worth filling in.

**Logos** (20 Oct 2026) were taken from each maker's own website: Biaxis (HLS banner), Classys, Dermalogica, Dermapen, Intraceuticals, Jeisys (recoloured from white), Mediderma, Neostrata, Celluma, Neauvia (icon only), Obagi (square), Pollogen, plus the Surface+ black logo from Drive. Still showing a typeset name: LHALA/H2MEDI, Liftera/Asterasys (site is JS-only), Rejuran (header file is icon-only), Profhilo, Nucleofill, Bellavita, Peplift, Thesera, Lanzox, Allergan, Tegoder (site down), Dermolissage, Athena, Dermashine, Immortal. Add a file under `assets/brands/` with the catalog's `logo` filename and it appears on the next build. The brands list now covers devices, injectables and boosters, professional peels and serums, and Surface+ home care, grouped by `category`.

## Testimonials

`catalog.json › testimonials.items` renders a "Kata mereka" section on the home page once an item has `publish: true`; until then the section shows only the Google-reviews links for each clinic (`clinics[].google_reviews`, currently the Maps links). Fields: name, clinic, treatment, quote / quote_en, source, date, optional `video_url` (a YouTube embed URL). Three customer review videos from January 2022 exist in Drive (CUSTOMER REVIEW VIDEOS, 130–245 MB each); they need consent re-confirmed and a YouTube upload before they can be embedded. Never paste Google review text without the reviewer's permission.

## Locations

`klinik.html` now embeds a Google Map per clinic (query-by-address embed, no API key), lists the doctors and devices at that clinic, and links to its Google reviews.

## Logo and photos

`assets/logo-mark.png` (the S mark, header) and `assets/logo-full.png` (mark + wordmark, footer and link previews) are cropped from `LOGO-01.png` in the Drive brand folder; `logo-full-white.png` is the white version for dark backgrounds. Doctor photos: `assets/doctors/` holds 1400 px versions of dr Riska, dr Devi, dr Kharisma and dr Nana, pulled from Drive › Doctors › Foto › edited (Sep 2026). dr Sukma's file is 11.4 MB, over the connector's 10 MB limit, so it still needs a smaller export. Doctors with photos are listed first. The Drive roster (Devi, Sukma, Kharisma, Riska, Nana) differs from the Q1 report roster (Riska, Hanna, Kharisma, Nana, Siti Aisyah): confirm who practises where before go-live, and set each doctor's `clinics`.

## Claims lint

`build.py` refuses to write anything if a rendered page contains a whitening or skin-lightening
claim. `BANNED` fails the build; `REVIEW` prints a warning and leaves the judgement to a person,
because a product name (`QS Brighten & Toning`) is a proper noun while a descriptive promise is
not. The menu currently raises five review warnings, three of them descriptive copy worth
rewriting around pigment and evenness.

To see it work, put `memutihkan` in any catalog field and run the build.

## 404

`404.html` is generated in both languages and carries `noindex`. A static host needs to be told to
serve it: `error_page 404 /404.html;` on nginx, a `404.html` at the root on GitHub Pages or
Netlify (automatic), or `"errorPage": "404.html"` on Cloudflare Pages. Without that line a bad URL
falls back to whatever the host does by default, which on the previous site was a blank page.

## Asset versioning

`style.css` and the JS files are linked with a short content hash (`style.css?v=c875ee13`), so a
returning visitor gets a changed stylesheet instead of the cached one. Nothing to maintain; the
hash is computed at build time.

## Skin analyzer (Analisis Kondisi Kulit)

`analisis.html` is the funnel's first step from the Three Flows doc: Ads → Smart Skin Assessment → free doctor consult. It runs the 13 intake questions from the Master Menu (Block A routes to a concern, Block B reads commitment, Block C is fit and safety), proposes the usual starting offer for that concern, and hands everything to WhatsApp as a structured message. The visitor picks the concern; the page never assigns a level, names a disease, or shows a discount.

**Photo scoring is off** (`catalog.json › assessment.scan.enabled: false`). No vendor was ever chosen. The strategy (`SSH_Digital_Product_Strategy.md` §5) says license a cosmetic-grade vendor, not build one, and not Skinive:

| Vendor | Why it fits |
|---|---|
| Perfect Corp (YouCam Skin Analysis API) | Aesthetic scores only, large API, used by beauty retail |
| Haut.AI | Aesthetic scores, B2B SaaS, white-label |
| Revieve | What ERHA Skin AIdentify runs on (112+ clinics) |
| Orbo | Aesthetic scores, Asia-focused |

To turn it on: sign a vendor, implement `window.SurfaceScan.analyze(file)` in `assets/scan-adapter.js` (contract is documented in the file), set `scan.enabled` to `true`, rebuild. Scores shown are pigmentasi, kerataan warna, flek, tekstur only. Ask the vendor the three questions in the adapter file first (on-device vs cloud, clinic-context terms, Fitzpatrick IV–V validation). Ship to 50% of traffic and measure booking rate before judging it.

## Hosting

Any static host works: GitHub Pages, Netlify, Cloudflare Pages, or the current hosting for surfaceskinhabit.com. Point the domain at the folder; there is no server code.

Local preview:

```bash
cd website && python3 -m http.server 8765
```

## Before go-live checklist

- [ ] Confirm which price list is current: the nine offers on the site are the 28 Sep review draft prices; the live Q4 promo set is Glass Skin Express / Clarity / Signature (Rp 899k–1.899jt to 30 Nov).
- [ ] Doctor sign-off on the combination sequences, timelines and interval table (education part two).
- [ ] Confirm clinic opening hours per branch (`hours_confirmed` is `false` for all four; mall hours 10.00–20.00 are assumed).
- [ ] Confirm the TSM Cibubur floor and unit number.
- [ ] Doctor consent (column X of `SSH_Doctor_Credentials_Form.xlsx`) for each doctor with `"publish": true`, then paste credentials into `bio` / `focus`.
- [ ] Add Instagram handle and email in `catalog.json › site` if they should appear in the footer.
- [ ] Skin analyzer vendor decision (see section above) before enabling the photo step.
- [ ] Surface+ home-care line: confirm the product list and prices to show (currently a single brand card with no products).
- [ ] Read the OORA battle card and adjust the USP if needed.
- [ ] dr Sukma needs a photo under 10 MB; confirm dr Devi's clinic and full name.
- [ ] Photos: hero, doctor, clinic and device photos are not included. Candidates are in Drive under *Surface Branding & Content* — `Stock Foto 1` (named per treatment), `Foto Dokter Png`, `Clinic Photo – for Content` (HEIC, needs conversion) and scattered device shots. The `Before After Liftera` set should not be used: before-and-after imagery is out of scope, and those look like manufacturer assets rather than Surface patients.
- [ ] Doctor sign-off on the education pages: every Fitzpatrick row, contraindication list and aftercare list.
- [ ] Tell the host to serve `404.html` (see the 404 section above).

## Stacks, add-ons, result photos (added 20 Oct 2026)
- `stacks.items[]`: signature one-visit combos (name, door, includes, duration_min, for, price, downtime, medical_review). Null price renders "at consultation". Shown on Harga (#stack), the home page, and each door page (its own door only).
- `addons[]`: seven add-ons per visit (name, treatment, for, price). Shown as a strip on Harga and every door page, and in the side card.
- `results.items[]`: before / week-12 photo pairs. A pair is only rendered when `publish`, `consent_on_file` and `doctor_signoff` are all set. The Tone door never shows photos (`results.doors_excluded`). Format example in `_results_item_format`. Put files under `assets/results/`.
