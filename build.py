#!/usr/bin/env python3
"""Build the Surface Skin Habit public website from catalog.json, in Indonesian and English.

    python3 build.py

Output:  index.html, menu.html, analisis.html, dokter.html, klinik.html   (Bahasa Indonesia, site root)
         en/index.html, en/menu.html, en/analisis.html, en/dokter.html, en/klinik.html   (English)
         sitemap.xml, robots.txt

Every customer-facing string comes from catalog.json (Indonesian field, plus a *_en twin) or from the
UI dictionary below. Pages are plain static HTML so search engines, WhatsApp previews and screen
readers can read the menu, prices, doctors and addresses. Each page links to its twin with hreflang.
"""
import json, html, datetime, pathlib, urllib.parse

ROOT = pathlib.Path(__file__).resolve().parent
C = json.loads((ROOT / "catalog.json").read_text(encoding="utf-8"))
S = C["site"]
TODAY = datetime.date.today().isoformat()
WA = "https://wa.me/" + S["whatsapp_number"]

def av(name):
    """assets/<name> with a short content hash, so a changed file is not served from cache."""
    import hashlib
    f = ROOT / "assets" / name
    h = hashlib.sha1(f.read_bytes()).hexdigest()[:8] if f.exists() else "0"
    return f"{PREFIX}assets/{name}?v={h}"
BASE = S["url"].rstrip("/")

# ---------------------------------------------------------------- UI strings
UI = {
  "id": {
    "nav": [("index.html#concern", "Program"), ("menu.html", "Harga"), ("analisis.html", "Analisis Kulit"), ("dokter.html", "Dokter"), ("klinik.html", "Klinik")], "f_more": "Lainnya", "f_edu": "Edukasi", "f_blog": "Blog", "f_fp": "Menu lengkap",
    "lang_switch": ("en/", "EN"), "lang_name": "Bahasa Indonesia",
    "wa_nav": "Booking via WhatsApp", "wa_nav_short": "Booking", "wa_nav_more": "via WhatsApp", "wa_bar": "Booking konsultasi dokter gratis",
    "generic_msg": "Halo Surface, saya mau booking konsultasi dokter gratis. Klinik terdekat saya: {klinik}.",
    "clinic_suffix": " Klinik terdekat saya: {klinik}.",
    "offer_msg": "Halo Surface, saya mau booking konsultasi dokter gratis untuk {offer} ({concern}). Klinik terdekat saya: {klinik}.",
    "fv_msg": "Halo Surface, saya mau booking level Start (Rp 799.000) + konsultasi dokter gratis. Klinik terdekat saya: {klinik}.",
    "plan_msg": "Halo Surface, saya tertarik Skin Habit Plan bulanan. Klinik terdekat saya: {klinik}.",
    "clinic_msg": "Halo Surface {clinic}, saya mau booking konsultasi dokter gratis.",
    "footer_tag": "Konsultasi dokter selalu gratis.", "f_clinics": "Klinik", "f_concern": "Concern", "f_doctors": "Dokter kami", "f_contact": "Hubungi",
    "f_legal": "Semua tindakan medis dilakukan oleh dokter. Hasil perawatan berbeda pada setiap orang.", "f_updated": "Harga diperbarui",
    "cta_h": "Mulai dari konsultasi dokter. Gratis.", "cta_p": "Chat kami, sebutkan concern dan klinik terdekat. Tim kami carikan jadwal konsultasi dokter, dan dokter yang menentukan level perawatanmu.",
    "cta_btn": "Chat WhatsApp sekarang", "cta_hours": "Dibalas",
    "level_word": "Level", "min": "menit", "single": "Satuan", "one_session": "1 sesi", "pack3": "Paket 3x", "pack6": "Paket 6x", "per_session": "/ sesi",
    "book_free": "Booking konsultasi gratis", "doctor_confirms": "Dokter memastikan treatment ini cocok untuk kulitmu sebelum dimulai.",
    "new_customers": "Pelanggan baru", "monthly": "Bulanan", "per_month": "/ bulan", "extras": "Tambahan", "addons_h": "Add-on per kunjungan",
    "addons_note": "Ditambahkan ke treatment mana pun atas saran dokter atau terapis.", "book_first": "Booking level Start", "ask_plan": "Tanya Skin Habit Plan",
    "open_maps": "Buka di Maps", "book_here": "Booking di sini",
    "hero_eyebrow": "Klinik kulit · {n} lokasi Jakarta", "hero_h1": "Kulit yang lebih baik dimulai dari konsultasi dokter. Gratis.",
    "hero_lead": "Pilih concern-mu. Dokter kami yang merekomendasikan treatment-nya. Harga terbuka, sama di semua klinik.",
    "hero_btn2": "Analisis kulit 2 menit", "trust": [("Dokter", "di setiap klinik"), ("Harga terbuka", "satuan, 3x, 6x"), ("Paket berlaku", "di 4 klinik")],
    "how": "Cara kerjanya", "steps": ["Pilih jalurmu: Clear, Tone, Texture, Calm, Tighten, atau Enhance.", "Datang untuk konsultasi dokter gratis di klinik terdekat.", "Dokter merekomendasikan treatment yang cocok untuk kulitmu.", "Pilih cara belinya: satuan, paket 3x, atau paket 6x."],
    "s1_eye": "Mulai dari sini", "s1_h": "Apa yang ingin kamu perbaiki?", "s1_p": "Tiga concern, masing-masing tiga pilihan treatment. Kamu memilih concern, dokter merekomendasikan treatment-nya.", "s1_btn": "Semua harga",
    "from": "Mulai", "per_session_long": "per sesi", "levels_short": "3 pilihan",
    "s2_eye": "Tiga level", "s2_h": "Dasar, Koreksi, Presisi", "s2_p": "Struktur level yang sama di setiap concern dan setiap klinik. Semakin tinggi level, semakin besar peran dokter.",
    "s3_eye": "Mulai", "s3_h": "Satu harga untuk mulai: Rp 799.000", "s3_p": "Level Start di setiap jalur: facial oleh terapis ditutup satu langkah dokter, satu kunjungan, satu harga. Atau program bulanan.",
    "s4_eye": "Tim medis", "s4_h": "Dokter kami", "s4_p": "Setiap treatment dengan alat, peeling medis, atau injeksi dilakukan oleh dokter. Konsultasi pertama selalu gratis.", "s4_btn": "Semua dokter",
    "s5_eye": "Lokasi", "s5_h": "Empat klinik, satu riwayat perawatan", "s5_p": "Sisa sesi paket dan riwayat perawatanmu berlaku di semua klinik Surface.", "s5_btn": "Alamat & Maps",
    "s6_eye": "Pertanyaan umum", "s6_h": "Yang sering ditanyakan",
    "t_index": "{name} · Klinik kulit dengan dokter di Jakarta, konsultasi gratis",
    "menu_eye": "Menu & harga", "menu_h1": "Harga terbuka. Sama di semua klinik.", "menu_lead_tail": "Di bawah ini tiga concern, masing-masing tiga pilihan treatment dari yang paling ringan, dengan harga satuan, paket 3x dan paket 6x.",
    "menu_tab_extra": "Plan & add-on", "menu_other": "Treatment lain di luar menu ini tetap tersedia melalui konsultasi dokter.",
    "menu_s2_eye": "Di luar paket", "menu_s2_h": "Level Start, plan bulanan, add-on",
    "t_menu": "Menu & Harga Treatment · {name}", "d_menu": "Harga treatment Surface Skin Habit: Clear (jerawat), Glow (kusam & flek), Lift (kekencangan). Harga satuan, paket 3x dan 6x. Konsultasi dokter gratis.",
    "doc_eye": "Tim medis", "doc_h1": "Dokter kami", "doc_lead": "Di Surface, dokter yang merekomendasikan treatment-mu, dan dokter pula yang melakukan setiap tindakan medis: peeling, laser, HIFU, injeksi. Konsultasi pertama selalu gratis, di klinik mana pun.",
    "doc_note": "Jadwal praktik dokter berbeda di setiap klinik. Sebutkan nama dokter saat booking jika kamu ingin bertemu dokter tertentu.",
    "t_doc": "Dokter Kami · {name}", "d_doc": "Dokter Surface Skin Habit di Setiabudi, CITOS, Lippo Mall Puri dan TSM Cibubur. Konsultasi dokter gratis untuk setiap pelanggan.",
    "cl_eye": "Lokasi", "cl_h1": "Empat klinik di Jakarta", "cl_lead": "Riwayat perawatan dan sisa sesi paketmu berlaku di keempat klinik. Pilih yang paling dekat. WhatsApp dibalas {hours}.",
    "t_cl": "Lokasi Klinik · {name}", "d_cl": "Alamat dan link Maps klinik Surface Skin Habit: Setiabudi, Cilandak Town Square (CITOS), Lippo Mall Puri, Trans Studio Mall Cibubur.",
    "edu_eye": "Edukasi", "edu_h1": "Cara kerja setiap alat dan tindakan",
    "edu_fam_h": "Kelompok alat", "edu_gloss_eye": "Istilah", "edu_gloss_h": "Kamus singkat",
    "edu_gloss_p": "Istilah yang sering muncul saat konsultasi, dijelaskan dalam bahasa sehari-hari.",
    "edu_all": "Semua alat & tindakan", "edu_back": "Kembali ke edukasi", "edu_learn": "Pelajari cara kerjanya",
    "edu_hubs": [("edukasi-treatment.html", "Treatment", "Semua treatment, siapa yang mengerjakan, berapa lama, seberapa sering, dan harga satuannya."),
                 ("edukasi-brand.html", "Alat & brand", "Alat dan produk apa yang dipakai, siapa pembuatnya, dan di treatment mana kamu menemuinya."),
                 ("edukasi-kombinasi.html", "Kombinasi", "Kenapa treatment dipasangkan, urutannya di kursi, dan apa yang berubah minggu demi minggu."),
                 ("edukasi-waktu.html", "Interval & waktu", "Jarak antar sesi, panjang program, masa berlaku paket, dan kapan harus menunda.")],
    "edu_devices_h": "Alat & tindakan: cara kerjanya", "edu_devices_p": "Satu halaman per alat: mekanisme, apa yang dirasakan, downtime, dan siapa yang sebaiknya menunda.",
    "vn_h": "Tiga hal yang kami gabungkan", "vn_p": "Dokter di setiap langkah, rencana yang bertanggal, dan kebiasaan bulanan. Klinik lain punya satu atau dua; Skin Habit adalah ketiganya sekaligus.", "vn_sets": [("Dokter", "menilai di setiap langkah"), ("Rencana", "program bertanggal, 12 minggu"), ("Kebiasaan", "satu kunjungan setiap bulan")], "vn_overlaps": [("Correct", "minggu 2\u201312"), ("Review", "minggu ke-12"), ("Maintain", "bulanan")], "vn_centre": ["SKIN", "HABIT"],
    "cy_name": "Siklus Skin Habit", "cy_tm": "\u2122", "cy_eye": "Cara kerja Surface", "cy_h": "Satu siklus, dokter di tengahnya", "cy_p": "Setiap pelanggan Surface bergerak dalam siklus yang sama, di jalur mana pun. Dokter menilai di setiap putaran; kamu hanya perlu datang sesuai jadwal.", "cy_btn": "Lihat siklusnya", "cy_centre": ["Dokter", "di setiap langkah"], "cy_more": "Pelajari Siklus Skin Habit",
    "cy_steps": [("Mulai", "Konsultasi dokter gratis + analisis kulit", "Kunjungan 1 \u00b7 20 menit", "Dokter melihat kulitmu, menyaring hal yang mengubah protokol, dan memilih jalurnya: Clear, Tone, Texture, Calm, Tighten, atau Enhance."), ("Start", "Satu kunjungan, satu harga: Rp 799.000", "Kunjungan 1 \u00b7 hari yang sama", "Facial oleh terapis ditutup satu langkah dokter. Kamu pulang dengan rencana tertulis: tanggal kunjungan berikutnya dan tanggal review."), ("Correct", "Program 3 atau 6 sesi", "Minggu 2\u201312 \u00b7 tiap 2\u20134 minggu", "Facial plus alat atau peeling medis oleh dokter, dijual sebagai program. Setiap kunjungan punya tanggal; kami yang mengingatkan."), ("Review", "Dokter menilai di minggu ke-12", "Minggu 12 \u00b7 foto ulang", "Foto dan analisis diulang dengan cahaya dan sudut yang sama. Dokter memutuskan: lanjut, naik ke Refine, atau pindah ke Maintain."), ("Maintain", "Satu kunjungan Start setiap bulan", "Bulanan \u00b7 Skin Habit Plan", "Hasil dijaga dengan kebiasaan, bukan paket baru. Setiap 12 minggu kembali ke Review.")],
    "cy_refine": ("Refine", "Alat atau injeksi paling terarah, hanya atas keputusan dokter di Review."),
    "t_cy": "Siklus Skin Habit \u00b7 Cara kerja {name}", "d_cy": "Siklus Skin Habit: Mulai, Start, Correct, Review minggu ke-12, Maintain. Cara setiap pelanggan Surface Skin Habit berjalan, dengan dokter di setiap langkah.",
    "sp_eye": "Ruang kami", "sp_h": "Klinik dan ruang treatment", "sp_btn": "Lihat semua klinik", "cl_photos": "Foto klinik", "sc_eye": "Level Start", "sc_h": "Mulai dari Rp 799.000", "sc_note": "Harga yang sama untuk semua pelanggan, baru maupun lama. Texture Start Rp 750.000; Enhance mulai dari konsultasi gratis.",
    "bs_eye": "Best seller", "bs_h": "Yang paling sering dipilih", "bs_where": "Ada di", "bs_badge": "Best seller", "bs_tab": "Best seller",
    "fp_eye": "Menu lengkap", "fp_h1": "Semua treatment & harga", "fp_tab": "Menu lengkap", "fp_programs": "18 program", "fp_singles": "Harga satuan", "fp_stacks": "Stack", "fp_addons": "Add-on", "fp_plan": "Plan bulanan", "t_fp": "Menu lengkap & harga · {name}", "d_fp": "Daftar lengkap treatment Surface Skin Habit dengan harga satuan, 18 program Start/Correct/Refine, stack, dan add-on. Harga sama di 4 klinik Jakarta.",
    "stk_eye": "Signature stacks", "stk_h": "Beberapa perawatan, satu kunjungan", "stk_one": "Satu kunjungan", "stk_for": "untuk", "stk_downtime": "ada downtime", "stk_before_h": "Sebelum stack", "stk_addons_h": "Tambah lagi", "stk_btn": "Lihat semua stack", "stk_msg": "Halo Surface, saya mau booking konsultasi dokter gratis untuk stack {stack}. Klinik terdekat saya: {klinik}.", "stk_door_h": "Stack untuk jalur ini", "stk_tab": "Stacks",
    "ad_eye": "Add-ons", "ad_h": "Tambahan di kunjungan yang sama", "ad_after_h": "Setelah program", "ad_fixed": "per kunjungan",
    "res_eye": "Hasil", "res_h": "Foto hasil pelanggan", "res_before": "Awal", "res_after": "Minggu ke-{w}", "res_rules_h": "Aturan foto hasil kami", "res_tone": "Untuk jalur Tone kami sengaja tidak memasang foto hasil. Baca aturannya di bawah.",
    "tx_eye": "Edukasi", "tx_h1": "Semua treatment di Surface", "tx_by": "Dikerjakan", "tx_dur": "Durasi", "tx_int": "Interval", "tx_for": "Untuk", "tx_price": "Harga satuan", "tx_brand": "Alat / brand", "tx_consult": "Saat konsultasi", "tx_device_link": "Cara kerja alatnya",
    "br_h1": "Alat & brand yang kami pakai", "br_maker": "Pembuat", "br_kind": "Jenis", "br_used": "Dipakai di", "br_origin": "Asal", "br_site": "Situs resmi", "br_reg": "Izin & sertifikasi", "br_at": "Tersedia di", "br_matrix_dev": "Alat", "br_strip_h": "Alat dan brand yang kami pakai", "br_strip_p": "Kami menyebut nama alatnya. Pembuat, negara asal, dan sertifikasinya ada di halaman Alat & brand.", "br_strip_btn": "Lihat semua alat & brand",
    "tm_eye": "Pelanggan", "tm_h": "Kata mereka", "tm_google_h": "Ulasan di Google", "tm_google_p": "Setiap klinik punya halaman ulasan Google sendiri. Baca langsung dari pelanggan.",
    "needs_review": "menunggu persetujuan Medical Lead", "next_door_h": "Pintu berikutnya", "front_door_h": "Mulai di sini, di jalur mana pun", "st_helped": "Bagaimana kami membantu", "st_for": "Ini untukmu kalau", "funnels_h": "Enam jalur, satu kebiasaan", "ig_h": "Dari Instagram kami", "ig_follow": "Ikuti @{h}", "ig_ph": "Tempel URL post Instagram di catalog.json › social.instagram.posts. Tiga tile ini akan diganti embed resmi Instagram.", "gr_h": "Ulasan Google per klinik", "gr_write": "Tulis ulasan", "gr_read": "Baca ulasan", "ph_label": "Placeholder desain", "blog_h": "Blog", "blog_lead": "Jawaban untuk pertanyaan yang masuk lewat WhatsApp, ditulis supaya kamu datang ke konsultasi dengan pertanyaan yang lebih tajam.", "blog_read": "Baca", "blog_back": "Semua artikel", "blog_cta": "Lihat programnya", "t_blog": "Blog · {name}", "d_blog": "Artikel Surface Skin Habit: harga treatment di Jakarta, perbandingan booster, bekas jerawat, dan cara memilih klinik kulit.", "cs_tpl": "Template WhatsApp", "cs_link": "Kirim tautan ini", "cs_copy": "Salin", "cs_copied": "Tersalin", "seo_kw": "Kata kunci", "seo_intent": "Intent", "seo_page": "Halaman", "seo_status": "Status", "st_journey": "Perjalanannya, minggu demi minggu", "st_offers": "Tiga pilihan treatment", "st_promise": "Yang kami janjikan", "st_not": "Yang tidak kami janjikan", "st_devices": "Alat yang dipakai di program ini", "st_faq": "Pertanyaan tentang program ini", "st_eye": "Program", "st_see_menu": "Lihat harga lengkap", "st_start": "Mulai program ini", "st_doctors": "Dokter yang menanganinya", "t_st": "{nav} · Program {name}", "d_st": "{lead}", "home_streams_btn": "Lihat programnya",
    "cl_map": "Peta", "cl_devices": "Alat di klinik ini", "cl_doctors": "Dokter di klinik ini", "cl_reviews": "Ulasan Google",
    "cb_h1": "Kombinasi treatment", "cb_rules_h": "Lima aturan kombinasi", "cb_seq_h": "Urutan di kursi, dan apa yang berubah kapan", "cb_seq_p": "Enam pola kombinasi yang dipakai menu Surface saat ini. Menit adalah perkiraan; dokter dan terapis menyesuaikan dengan kulitmu.", "cb_steps": "Urutan di kursi", "cb_timeline": "Yang berubah, kapan", "cb_offers": "Dipakai di", "cb_not_h": "Yang tidak dipasangkan dalam satu kunjungan", "cb_not_a": "Ini", "cb_not_b": "dengan", "cb_not_why": "Kenapa", "cb_total": "total",
    "tm_h1": "Interval, program & waktu tunggu", "tm_int_h": "Jarak antar sesi per jenis treatment", "tm_what": "Treatment", "tm_int": "Interval", "tm_series": "Seri", "tm_why": "Kenapa", "tm_course_h": "Panjang program & masa berlaku", "tm_wait_h": "Kapan harus menunda", "tm_rebook_h": "Kapan kunjungan berikutnya", "tm_rebook_p": "Jadwal kunjungan berikutnya dibuat sebelum kamu pulang, bukan lewat pesan menyusul.",
    "t_tx": "Semua Treatment · {name}", "d_tx": "Daftar treatment Surface Skin Habit: facial, peeling medis, laser, RF, HIFU, microneedling, injeksi. Siapa yang mengerjakan, durasi, interval, dan harga satuan.",
    "t_br": "Alat & Brand · {name}", "d_br": "Alat dan brand yang dipakai Surface Skin Habit: LHALA Peel H2MEDI, Biaxis Nd:YAG, Cellec V IPL, Liftera HIFU, Pollogen RF, Nanopore, Celluma PDT, Aquapure, Tegoder, dan lainnya.",
    "t_cb": "Kombinasi Treatment · {name}", "d_cb": "Kenapa treatment di Surface dikombinasikan, urutan di kursi, timeline hasil minggu demi minggu, dan pasangan yang tidak boleh satu kunjungan.",
    "t_tm": "Interval & Waktu Treatment · {name}", "d_tm": "Jarak antar sesi untuk facial, peeling, laser, RF, HIFU, microneedling dan injeksi; panjang program; masa berlaku paket; kapan harus menunda treatment.",
    "edu_disclaimer_h": "Ini bukan diagnosis",
    "t_edu": "Edukasi Treatment & Alat · {name}",
    "d_edu": "Penjelasan cara kerja alat dan tindakan di Surface Skin Habit: laser, IPL, HIFU, RF, microneedling, LED, facial dan peeling medis. Durasi, jarak antar sesi, downtime dan tipe kulit.",
    "t_dev": "{dev} · Cara kerjanya · {name}", "d_dev": "{how} Durasi {dur} menit, {interval}. Dilakukan oleh {by} di {clinics}.",
    "dev_how": "Cara kerjanya", "dev_detail": "Lebih dalam", "dev_treats": "Untuk kondisi kulit",
    "dev_spec": "Ringkasan", "dev_dur": "Durasi satu sesi", "dev_int": "Jarak antar sesi", "dev_down": "Downtime",
    "dev_feel": "Rasanya", "dev_by": "Dilakukan oleh", "dev_at": "Tersedia di", "dev_type": "Jenis alat",
    "dev_fitz": "Tipe kulit", "dev_fitz_p": "Skala Fitzpatrick mengelompokkan kulit berdasarkan reaksinya terhadap matahari. Sebagian besar pelanggan kami berada di tipe III–IV.",
    "dev_avoid": "Tunda dulu bila", "dev_after": "Setelah tindakan", "dev_related": "Concern terkait",
    "by_doctor": "Dokter", "by_therapist": "Terapis",
    "fam_all_clinics": "Semua klinik",
    "e404_eye": "404", "e404_h": "Halaman ini tidak ada", "e404_p": "Alamat yang kamu buka tidak kami temukan. Mungkin tautannya sudah berubah. Coba salah satu halaman di bawah ini.",
    "e404_home": "Ke beranda", "t_404": "Halaman tidak ditemukan · {name}",
    "aq_eye": "Langkah pertama", "aq_noscript": "Formulir ini membutuhkan JavaScript. Kamu juga bisa langsung chat WhatsApp dan tim kami akan menanyakan hal yang sama.", "aq_block": "Blok",
    "aq_cards": [("Kamu memilih concern", "Jawabanmu menentukan concern: Clear, Glow, atau Lift, dan titik mulai yang biasanya disarankan."),
                 ("Dokter merekomendasikan treatment", "Hasil ini dibawa ke konsultasi dokter gratis. Dokter yang memastikan treatment mana yang cocok."),
                 ("Tidak ada diagnosis", "Ini analisis kondisi kulit, bukan diagnosis. Jawaban soal kehamilan atau obat hanya membantu dokter menyiapkan konsultasimu.")],
    "t_aq": "Analisis Kondisi Kulit · {name}", "d_aq": "Analisis kondisi kulit 2 menit dari Surface Skin Habit: 13 pertanyaan untuk menentukan concern (Clear, Glow, Lift) dan treatment awal yang biasanya disarankan. Bukan pengganti konsultasi dokter gratis.",
    "aq_js": {"of": "dari", "next": "Lanjut", "skip": "Lewati", "back": "Kembali", "yes": "Ya", "no": "Tidak", "pick_photo": "Pilih atau ambil foto",
              "cosmetic": "Pembacaan kosmetik, bukan diagnosis. Bisa dilewati.", "scan_na": "Scan belum tersedia.", "analyzing": "Menganalisis…",
              "scan_fail": "Foto tidak bisa diproses. Lewati saja, dokter akan melihat langsung.", "result": "Hasil", "best_concern": "Jalur yang paling cocok", "your_type": "Tipe kulitmu", "type_facial": "Facial yang cocok", "type_care": "Rutinitas harian", "m_type": "Tipe kulit", "start_with": "Mulai dengan",
              "usual_start": "Titik mulai yang biasanya disarankan", "min": "menit", "single": "satuan", "pack3": "paket 3x", "pack6": "paket 6x", "per_session": "/sesi", "from": "mulai", "per_session_long": "per sesi",
              "levels": {"L1": "Dasar", "L2": "Koreksi", "L3": "Presisi"}, "flag_pre": "Kamu menjawab \"ya\" untuk: ", "flag_post": ". Dokter akan membahasnya dulu di konsultasi, dan bisa menyesuaikan rencananya.",
              "send": "Kirim hasil & booking via WhatsApp", "see_all": "Lihat semua pilihan", "restart": "Ulangi",
              "m_head": "Halo Surface, saya sudah isi Analisis Kondisi Kulit di website.", "m_concern": "Concern", "m_also": "Juga", "m_since": "Sudah", "m_tried": "Sudah coba",
              "m_freq": "Bisa datang", "m_start": "Mau mulai", "m_hope": "Harapan 3 bulan", "m_flags": "Perlu diketahui dokter", "m_scan": "Skor scan",
              "m_clinic": "Klinik terdekat saya: {klinik}. ", "m_tail": "Mau booking konsultasi dokter gratis."},
  },
  "en": {
    "nav": [("index.html#concern", "Programmes"), ("menu.html", "Prices"), ("analisis.html", "Skin Analysis"), ("dokter.html", "Doctors"), ("klinik.html", "Clinics")], "f_more": "More", "f_edu": "Education", "f_blog": "Blog", "f_fp": "Full menu",
    "lang_switch": ("../", "ID"), "lang_name": "English",
    "wa_nav": "Book via WhatsApp", "wa_nav_short": "Book", "wa_nav_more": "via WhatsApp", "wa_bar": "Book a free doctor consultation",
    "generic_msg": "Hi Surface, I'd like to book a free doctor consultation. My nearest clinic: {klinik}.",
    "clinic_suffix": " My nearest clinic: {klinik}.",
    "offer_msg": "Hi Surface, I'd like to book a free doctor consultation for {offer} ({concern}). My nearest clinic: {klinik}.",
    "fv_msg": "Hi Surface, I'd like to book the Start level (Rp 799,000) + free doctor consultation. My nearest clinic: {klinik}.",
    "plan_msg": "Hi Surface, I'm interested in the monthly Skin Habit Plan. My nearest clinic: {klinik}.",
    "clinic_msg": "Hi Surface {clinic}, I'd like to book a free doctor consultation.",
    "footer_tag": "Doctor consultation is always free.", "f_clinics": "Clinics", "f_concern": "Concern", "f_doctors": "Our doctors", "f_contact": "Contact",
    "f_legal": "All medical procedures are performed by doctors. Results vary from person to person.", "f_updated": "Prices updated",
    "cta_h": "Start with a doctor consultation. Free.", "cta_p": "Message us with your concern and nearest clinic. We'll find you a doctor consultation slot, and the doctor decides your treatment level.",
    "cta_btn": "Chat on WhatsApp now", "cta_hours": "Replies",
    "level_word": "Level", "min": "min", "single": "Single", "one_session": "1 session", "pack3": "3-session pack", "pack6": "6-session pack", "per_session": "/ session",
    "book_free": "Book a free consultation", "doctor_confirms": "The doctor confirms this treatment suits your skin before it starts.",
    "new_customers": "New customers", "monthly": "Monthly", "per_month": "/ month", "extras": "Extras", "addons_h": "Add-ons per visit",
    "addons_note": "Added to any treatment on the advice of the doctor or therapist.", "book_first": "Book the Start level", "ask_plan": "Ask about the Skin Habit Plan",
    "open_maps": "Open in Maps", "book_here": "Book here",
    "hero_eyebrow": "Skin clinic · {n} Jakarta locations", "hero_h1": "Better skin starts with a doctor consultation. Free.",
    "hero_lead": "Pick your concern. Our doctors recommend the treatment. Open pricing, the same at every clinic.",
    "hero_btn2": "2-minute skin analysis", "trust": [("Doctors", "at every clinic"), ("Open pricing", "single, 3x, 6x"), ("Packages valid", "at all 4 clinics")],
    "how": "How it works", "steps": ["Pick your pathway: Clear, Tone, Texture, Calm, Tighten, or Enhance.", "Come in for a free doctor consultation at your nearest clinic.", "The doctor recommends the treatment that suits your skin.", "Choose how to buy: single, 3-session, or 6-session."],
    "s1_eye": "Start here", "s1_h": "What would you like to improve?", "s1_p": "Three concerns, three treatment options each. You choose the concern, the doctor recommends the treatment.", "s1_btn": "All prices",
    "from": "From", "per_session_long": "per session", "levels_short": "3 options",
    "s2_eye": "Three levels", "s2_h": "Core, Correct, Refine", "s2_p": "The same level structure for every concern at every clinic. The higher the level, the bigger the doctor's role.",
    "s3_eye": "Start", "s3_h": "One price to start: Rp 799,000", "s3_p": "The Start level in every pathway: a therapist facial closed with one doctor step, one visit, one price. Or a monthly programme.",
    "s4_eye": "Medical team", "s4_h": "Our doctors", "s4_p": "Every treatment with a device, medical peel or injectable is performed by a doctor. The first consultation is always free.", "s4_btn": "All doctors",
    "s5_eye": "Locations", "s5_h": "Four clinics, one treatment history", "s5_p": "Your remaining package sessions and treatment history are valid at every Surface clinic.", "s5_btn": "Addresses & Maps",
    "s6_eye": "FAQ", "s6_h": "Frequently asked",
    "t_index": "{name} · Doctor-led skin clinic in Jakarta, free consultation",
    "menu_eye": "Menu & prices", "menu_h1": "Open pricing. The same at every clinic.", "menu_lead_tail": "Below: three concerns, three treatment options each from the gentlest up, with single, 3-session and 6-session prices.",
    "menu_tab_extra": "Plan & add-ons", "menu_other": "Other treatments outside this menu remain available through a doctor consultation.",
    "menu_s2_eye": "Outside packages", "menu_s2_h": "Start level, monthly plan, add-ons",
    "t_menu": "Treatment Menu & Prices · {name}", "d_menu": "Surface Skin Habit treatment prices: Clear (acne), Glow (dullness & spots), Lift (firmness). Single, 3-session and 6-session prices. Free doctor consultation.",
    "doc_eye": "Medical team", "doc_h1": "Our doctors", "doc_lead": "At Surface, a doctor recommends your treatment, and a doctor performs every medical procedure: peels, laser, HIFU, injectables. The first consultation is always free, at any clinic.",
    "doc_note": "Doctor schedules differ by clinic. Mention the doctor's name when booking if you'd like to see someone specific.",
    "t_doc": "Our Doctors · {name}", "d_doc": "Surface Skin Habit doctors at Setiabudi, CITOS, Lippo Mall Puri and TSM Cibubur. Free doctor consultation for every customer.",
    "cl_eye": "Locations", "cl_h1": "Four clinics in Jakarta", "cl_lead": "Your treatment history and remaining sessions are valid at all four clinics. Pick the nearest. WhatsApp replies {hours}.",
    "t_cl": "Clinic Locations · {name}", "d_cl": "Addresses and Maps links for Surface Skin Habit clinics: Setiabudi, Cilandak Town Square (CITOS), Lippo Mall Puri, Trans Studio Mall Cibubur.",
    "edu_eye": "Education", "edu_h1": "How each device and procedure works",
    "edu_fam_h": "Device groups", "edu_gloss_eye": "Terms", "edu_gloss_h": "A short glossary",
    "edu_gloss_p": "The terms that come up most often in consultation, explained in plain language.",
    "edu_all": "All devices & procedures", "edu_back": "Back to education", "edu_learn": "How it works",
    "edu_hubs": [("edukasi-treatment.html", "Treatments", "Every treatment, who performs it, how long, how often, and the single-session price."),
                 ("edukasi-brand.html", "Devices & brands", "Which devices and products are used, who makes them, and where you will meet them."),
                 ("edukasi-kombinasi.html", "Combinations", "Why treatments are paired, the order in the chair, and what changes week by week."),
                 ("edukasi-waktu.html", "Intervals & timing", "Gaps between sessions, programme length, package validity, and when to wait.")],
    "edu_devices_h": "Devices & procedures: how they work", "edu_devices_p": "One page per device: mechanism, what it feels like, downtime, and who should wait.",
    "vn_h": "Three things we combine", "vn_p": "A doctor at every step, a plan with dates, and a monthly habit. Other clinics have one or two; Skin Habit is all three at once.", "vn_sets": [("Doctor", "assesses at every step"), ("Plan", "dated programme, 12 weeks"), ("Habit", "one visit every month")], "vn_overlaps": [("Correct", "weeks 2\u201312"), ("Review", "week 12"), ("Maintain", "monthly")], "vn_centre": ["SKIN", "HABIT"],
    "cy_name": "The Skin Habit Cycle", "cy_tm": "\u2122", "cy_eye": "How Surface works", "cy_h": "One cycle, with the doctor at its centre", "cy_p": "Every Surface customer moves through the same cycle, whichever pathway they are on. The doctor assesses on every turn; you only need to show up on schedule.", "cy_btn": "See the cycle", "cy_centre": ["Doctor", "at every step"], "cy_more": "Learn the Skin Habit Cycle",
    "cy_steps": [("Begin", "Free doctor consultation + skin analysis", "Visit 1 \u00b7 20 min", "The doctor looks at your skin, screens for anything that changes the protocol, and picks the pathway: Clear, Tone, Texture, Calm, Tighten or Enhance."), ("Start", "One visit, one price: Rp 799,000", "Visit 1 \u00b7 same day", "A therapist facial closed with one doctor step. You leave with a written plan: the next visit date and the review date."), ("Correct", "A 3- or 6-session programme", "Weeks 2\u201312 \u00b7 every 2\u20134 weeks", "Facial plus a device or medical peel by the doctor, sold as a programme. Every visit has a date; we do the reminding."), ("Review", "The doctor assesses at week 12", "Week 12 \u00b7 photos repeated", "Photos and analysis repeated with the same light and angle. The doctor decides: continue, step up to Refine, or move to Maintain."), ("Maintain", "One Start visit every month", "Monthly \u00b7 Skin Habit Plan", "Results kept by habit, not by a new package. Every 12 weeks, back to Review.")],
    "cy_refine": ("Refine", "The most targeted device or injectable, only on the doctor's decision at Review."),
    "t_cy": "The Skin Habit Cycle \u00b7 How {name} works", "d_cy": "The Skin Habit Cycle: Begin, Start, Correct, Review at week 12, Maintain. How every Surface Skin Habit customer moves, with a doctor at every step.",
    "sp_eye": "Our spaces", "sp_h": "Clinics and treatment rooms", "sp_btn": "See all clinics", "cl_photos": "Clinic photos", "sc_eye": "Start level", "sc_h": "From Rp 799,000", "sc_note": "The same price for every customer, new or returning. Texture Start Rp 750,000; Enhance starts with a free consultation.",
    "bs_eye": "Best sellers", "bs_h": "What people choose most", "bs_where": "Found in", "bs_badge": "Best seller", "bs_tab": "Best sellers",
    "fp_eye": "Full menu", "fp_h1": "Every treatment & price", "fp_tab": "Full menu", "fp_programs": "18 programmes", "fp_singles": "Single-session prices", "fp_stacks": "Stacks", "fp_addons": "Add-ons", "fp_plan": "Monthly plan", "t_fp": "Full menu & prices · {name}", "d_fp": "The complete Surface Skin Habit treatment list with single prices, 18 Start/Correct/Refine programmes, stacks and add-ons. Same prices at 4 Jakarta clinics.",
    "stk_eye": "Signature stacks", "stk_h": "Several treatments, one visit", "stk_one": "One visit", "stk_for": "for", "stk_downtime": "has downtime", "stk_before_h": "Before a stack", "stk_addons_h": "Add more", "stk_btn": "See all stacks", "stk_msg": "Hello Surface, I'd like to book a free doctor consultation for the {stack} stack. My nearest clinic: {klinik}.", "stk_door_h": "The stack for this pathway", "stk_tab": "Stacks",
    "ad_eye": "Add-ons", "ad_h": "Extras in the same visit", "ad_after_h": "After a programme", "ad_fixed": "per visit",
    "res_eye": "Results", "res_h": "Customer result photos", "res_before": "Start", "res_after": "Week {w}", "res_rules_h": "Our rules for result photos", "res_tone": "For the Tone pathway we deliberately show no result photos. Read the rules below.",
    "tx_eye": "Education", "tx_h1": "Every treatment at Surface", "tx_by": "Performed by", "tx_dur": "Duration", "tx_int": "Interval", "tx_for": "For", "tx_price": "Single price", "tx_brand": "Device / brand", "tx_consult": "At consultation", "tx_device_link": "How the device works",
    "br_h1": "The devices & brands we use", "br_maker": "Maker", "br_kind": "Type", "br_used": "Used in", "br_origin": "Origin", "br_site": "Official site", "br_reg": "Clearances & certification", "br_at": "Available at", "br_matrix_dev": "Device", "br_strip_h": "The devices and brands we use", "br_strip_p": "We name our devices. Maker, country of origin and certifications are on the Devices & brands page.", "br_strip_btn": "See all devices & brands",
    "tm_eye": "Customers", "tm_h": "In their words", "tm_google_h": "Reviews on Google", "tm_google_p": "Every clinic has its own Google reviews page. Read them straight from customers.",
    "needs_review": "awaiting Medical Lead sign-off", "next_door_h": "Next door", "front_door_h": "Start here, in any pathway", "st_helped": "How we have helped", "st_for": "This is for you if", "funnels_h": "Six pathways, one habit", "ig_h": "From our Instagram", "ig_follow": "Follow @{h}", "ig_ph": "Paste Instagram post URLs into catalog.json › social.instagram.posts. These three tiles become official Instagram embeds.", "gr_h": "Google reviews by clinic", "gr_write": "Write a review", "gr_read": "Read reviews", "ph_label": "Design placeholder", "blog_h": "Blog", "blog_lead": "Answers to the questions that arrive on WhatsApp, written so you come to the consultation with sharper questions.", "blog_read": "Read", "blog_back": "All articles", "blog_cta": "See the programme", "t_blog": "Blog · {name}", "d_blog": "Surface Skin Habit articles: treatment prices in Jakarta, booster comparisons, acne scars, and how to choose a skin clinic.", "cs_tpl": "WhatsApp template", "cs_link": "Send this link", "cs_copy": "Copy", "cs_copied": "Copied", "seo_kw": "Keyword", "seo_intent": "Intent", "seo_page": "Page", "seo_status": "Status", "st_journey": "The journey, week by week", "st_offers": "Three treatment options", "st_promise": "What we promise", "st_not": "What we don't promise", "st_devices": "Devices used in this programme", "st_faq": "Questions about this programme", "st_eye": "Programme", "st_see_menu": "See full prices", "st_start": "Start this programme", "st_doctors": "The doctors who run it", "t_st": "{nav} · {name} Programme", "d_st": "{lead}", "home_streams_btn": "See the programme",
    "cl_map": "Map", "cl_devices": "Devices at this clinic", "cl_doctors": "Doctors at this clinic", "cl_reviews": "Google reviews",
    "cb_h1": "Treatment combinations", "cb_rules_h": "Five rules of combining", "cb_seq_h": "The order in the chair, and what changes when", "cb_seq_p": "The six combination patterns on the current Surface menu. Minutes are estimates; the doctor and therapist adjust to your skin.", "cb_steps": "Order in the chair", "cb_timeline": "What changes, when", "cb_offers": "Used in", "cb_not_h": "What is not paired in one visit", "cb_not_a": "This", "cb_not_b": "with", "cb_not_why": "Why", "cb_total": "total",
    "tm_h1": "Intervals, programmes & waiting times", "tm_int_h": "Gap between sessions by treatment type", "tm_what": "Treatment", "tm_int": "Interval", "tm_series": "Series", "tm_why": "Why", "tm_course_h": "Programme length & validity", "tm_wait_h": "When to wait", "tm_rebook_h": "When your next visit should be", "tm_rebook_p": "Your next appointment is booked before you leave, not chased by message afterwards.",
    "t_tx": "All Treatments · {name}", "d_tx": "Surface Skin Habit treatment list: facials, medical peels, laser, RF, HIFU, microneedling, injectables. Who performs each, duration, interval and single-session price.",
    "t_br": "Devices & Brands · {name}", "d_br": "Devices and brands used at Surface Skin Habit: LHALA Peel H2MEDI, Biaxis Nd:YAG, Cellec V IPL, Liftera HIFU, Pollogen RF, Nanopore, Celluma PDT, Aquapure, Tegoder and more.",
    "t_cb": "Treatment Combinations · {name}", "d_cb": "Why Surface combines treatments, the order in the chair, a week-by-week results timeline, and the pairs that do not share a visit.",
    "t_tm": "Treatment Intervals & Timing · {name}", "d_tm": "Gaps between sessions for facials, peels, laser, RF, HIFU, microneedling and injectables; programme length; package validity; when to postpone a treatment.",
    "edu_disclaimer_h": "This is not a diagnosis",
    "t_edu": "Treatment & Device Education · {name}",
    "d_edu": "How the devices and procedures at Surface Skin Habit work: laser, IPL, HIFU, RF, microneedling, LED, facials and medical peels. Duration, interval, downtime and skin types.",
    "t_dev": "{dev} · How it works · {name}", "d_dev": "{how} {dur} minutes per session, {interval}. Performed by a {by} at {clinics}.",
    "dev_how": "How it works", "dev_detail": "In more depth", "dev_treats": "What it is used for",
    "dev_spec": "At a glance", "dev_dur": "Session length", "dev_int": "Interval between sessions", "dev_down": "Downtime",
    "dev_feel": "What it feels like", "dev_by": "Performed by", "dev_at": "Available at", "dev_type": "Device type",
    "dev_fitz": "Skin types", "dev_fitz_p": "The Fitzpatrick scale groups skin by how it reacts to sun. Most of our customers sit at types III–IV.",
    "dev_avoid": "Wait if", "dev_after": "Afterwards", "dev_related": "Related concern",
    "by_doctor": "a doctor", "by_therapist": "a therapist",
    "fam_all_clinics": "All clinics",
    "e404_eye": "404", "e404_h": "This page does not exist", "e404_p": "We couldn't find the address you opened. The link may have changed. Try one of the pages below.",
    "e404_home": "Go to the homepage", "t_404": "Page not found · {name}",
    "aq_eye": "First step", "aq_noscript": "This form needs JavaScript. You can also message us on WhatsApp and our team will ask the same questions.", "aq_block": "Block",
    "aq_cards": [("You pick the concern", "Your answers point to a concern: Clear, Glow, or Lift, and the usual starting point."),
                 ("The doctor recommends the treatment", "Bring the result to your free doctor consultation. The doctor confirms which treatment fits."),
                 ("No diagnosis", "This is a skin condition analysis, not a diagnosis. Questions about pregnancy or medication only help the doctor prepare your consultation.")],
    "t_aq": "Skin Condition Analysis · {name}", "d_aq": "2-minute skin condition analysis from Surface Skin Habit: 13 questions to find your concern (Clear, Glow, Lift) and the usual first treatment. Not a substitute for the free doctor consultation.",
    "aq_js": {"of": "of", "next": "Next", "skip": "Skip", "back": "Back", "yes": "Yes", "no": "No", "pick_photo": "Choose or take a photo",
              "cosmetic": "A cosmetic reading, not a diagnosis. You can skip this.", "scan_na": "Scan not available yet.", "analyzing": "Analysing…",
              "scan_fail": "The photo couldn't be processed. Skip it, the doctor will look in person.", "result": "Result", "best_concern": "Best-matching concern", "your_type": "Your skin type", "type_facial": "The facial that fits", "type_care": "Daily routine", "m_type": "Skin type", "start_with": "Start with",
              "usual_start": "Usual starting point", "min": "min", "single": "single", "pack3": "3-session pack", "pack6": "6-session pack", "per_session": "/session", "from": "from", "per_session_long": "per session",
              "levels": {"L1": "Core", "L2": "Correct", "L3": "Refine"}, "flag_pre": "You answered \"yes\" to: ", "flag_post": ". The doctor will discuss this first at the consultation and can adjust the plan.",
              "send": "Send result & book via WhatsApp", "see_all": "See all options for", "restart": "Start over",
              "m_head": "Hi Surface, I completed the Skin Condition Analysis on the website.", "m_concern": "Concern", "m_also": "Also", "m_since": "Since", "m_tried": "Tried",
              "m_freq": "Can come in", "m_start": "Want to start with", "m_hope": "Hope in 3 months", "m_flags": "Doctor should know", "m_scan": "Scan scores",
              "m_clinic": "My nearest clinic: {klinik}. ", "m_tail": "I'd like to book a free doctor consultation."},
  },
}

# ---------------------------------------------------------------- language state
L = "id"           # current language, set by the build loop
PREFIX = ""        # "" for root, "../" for en/
def T(key, **kw):
    v = UI[L][key]
    return v.format(**kw) if kw and isinstance(v, str) else v
def t(obj, key):
    """Catalog text in the current language: obj[key_en] when building English and present, else obj[key]."""
    if L == "en" and (key + "_en") in obj:
        return obj[key + "_en"]
    return obj[key]

# ---------------------------------------------------------------- helpers
def e(s):
    return html.escape(str(s), quote=True)
def rp(n):
    return "Rp " + f"{int(n):,}".replace(",", ".")
def wa_link(msg):
    return WA + "?text=" + urllib.parse.quote(msg)
WA_ICO = ('<svg class="ico" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
          '<path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.25-1.38c1.45.79 3.08 1.21 4.79 1.21 5.46 0 9.91-4.45 9.91-9.91S17.5 2 12.04 2m0 1.67c4.54 0 8.24 3.7 8.24 8.24s-3.7 8.24-8.24 8.24c-1.52 0-3-.42-4.29-1.2l-.31-.18-3.12.82.83-3.04-.2-.32a8.2 8.2 0 0 1-1.26-4.36c0-4.54 3.7-8.24 8.24-8.24M8.53 7.33c-.16 0-.43.06-.66.31-.22.25-.87.86-.87 2.07 0 1.22.89 2.39 1 2.56.14.17 1.76 2.67 4.25 3.73.59.27 1.05.42 1.41.53.59.19 1.13.16 1.56.1.48-.07 1.46-.6 1.67-1.18.21-.58.21-1.07.15-1.18-.07-.1-.23-.16-.48-.27-.25-.14-1.47-.74-1.69-.82-.23-.08-.37-.12-.56.12-.16.25-.64.81-.78.97-.15.17-.29.19-.53.07-.26-.13-1.06-.39-2-1.23-.74-.66-1.23-1.47-1.38-1.72-.12-.24-.01-.39.11-.5.11-.11.27-.29.37-.44.13-.14.17-.25.25-.41.08-.17.04-.31-.02-.43-.06-.11-.56-1.35-.77-1.84-.2-.48-.4-.42-.56-.43-.14 0-.3-.01-.47-.01"/></svg>')
def wa_btn(msg, label, cls="btn btn-wa", extra=""):
    # Server-rendered link carries no clinic; site.js fills "{klinik}" in when the visitor has picked one.
    plain = msg.replace(T("clinic_suffix"), "")
    return f'<a class="{cls}" href="{wa_link(plain)}" data-wa-msg="{e(msg)}" target="_blank" rel="noopener" {extra}>{WA_ICO}{e(label)}</a>'
def clinic(code):
    return next(c for c in C["clinics"] if c["code"] == code)
def min_single(concern):
    return min(o["single"] for o in concern["offers"] if o.get("single"))
def page_url(path, lang):
    p = "" if path == "index.html" else path
    return BASE + "/" + ("en/" if lang == "en" else "") + p
def alt_path(path, lang):
    """Stream and blog pages have a different filename per language; everything else keeps its name."""
    for st in C["streams"].values():
        if path in (st["slug"] + ".html", st["slug_en"] + ".html"):
            return (st["slug_en"] if lang == "en" else st["slug"]) + ".html"
    for x in C.get("posts", []):
        if path in ("blog-" + x["slug"] + ".html", "blog-" + x["slug_en"] + ".html"):
            return "blog-" + (x["slug_en"] if lang == "en" else x["slug"]) + ".html"
    return path
def slug(name):
    return name.lower().replace(" ", "-").replace("&", "and")

# ---------------------------------------------------------------- shell
def head(title, desc, path, jsonld=None):
    ld = "".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>" for x in (jsonld or []))
    return f"""<!doctype html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{e(page_url(path, L))}">
<link rel="alternate" hreflang="id" href="{e(page_url(alt_path(path, 'id'), 'id'))}">
<link rel="alternate" hreflang="en" href="{e(page_url(alt_path(path, 'en'), 'en'))}">
<link rel="alternate" hreflang="x-default" href="{e(page_url(alt_path(path, 'id'), 'id'))}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(S['name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{e(page_url(path, L))}">
<meta property="og:locale" content="{'en_US' if L == 'en' else 'id_ID'}">
<meta property="og:image" content="{BASE}/assets/logo-full.png">
<meta name="theme-color" content="#FBF7F4">
<link rel="apple-touch-icon" href="{PREFIX}assets/logo-mark.png">
<link rel="icon" href="{PREFIX}assets/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{av("style.css")}">
{ld}
</head>
<body>
"""

def header(active, path=None):
    links = ""
    for h, label in T("nav"):
        cur = ' aria-current="page"' if h == active else ""
        links += f'<li><a href="{h}"{cur}>{e(label)}</a></li>'
    sw_href, sw_label = T("lang_switch")
    other = "English" if L == "id" else "Bahasa Indonesia"
    other_code = "en" if L == "id" else "id"
    here = path or active
    sw_target = sw_href + ("" if here == "index.html" else alt_path(here, other_code))
    return f"""<header class="site-header">
  <div class="wrap nav">
    <a class="logo" href="index.html" aria-label="{e(S['name'])}"><img class="mark-img" src="{PREFIX}assets/logo-mark.png" alt="" width="30" height="48"><span class="wordmark"><span class="l1">SURFACE</span><span class="l2">SKIN HABIT</span></span></a>
    <nav aria-label="Main"><ul class="nav-links">{links}<li><a class="lang" href="{sw_target}" hreflang="{other_code}" lang="{other_code}" title="{e(other)}">{e(sw_label)}</a></li></ul></nav>
    <div class="nav-cta">
      <a class="btn btn-wa btn-sm nav-wa" href="{wa_link(T("generic_msg").replace(T("clinic_suffix"), ""))}" data-wa-msg="{e(T("generic_msg"))}" target="_blank" rel="noopener">{WA_ICO}{e(T("wa_nav_short"))}<span class="nav-wa-more"> {e(T("wa_nav_more"))}</span></a>
      <a class="lang lang-mobile" href="{sw_target}" hreflang="{other_code}" lang="{other_code}" title="{e(other)}">{e(sw_label)}</a>
      <button class="nav-toggle" aria-label="Menu" aria-expanded="false"><span></span></button>
    </div>
  </div>
</header>
<main>
"""

def footer():
    clinics = "".join(f'<li><a href="klinik.html#{c["code"].lower()}">{e(c["short"])}</a><span class="muted small"> · {e(t(c, "area"))}</span></li>' for c in C["clinics"])
    concerns = "".join(f'<li><a href="{stream_file(c["code"])}">{e(t(c, "title"))}</a></li>' for c in C["concerns"])
    ig = f'<li><a href="https://instagram.com/{e(S["instagram"].lstrip("@"))}" target="_blank" rel="noopener">Instagram @{e(S["instagram"].lstrip("@"))}</a></li>' if S.get("instagram") else ""
    em = f'<li><a href="mailto:{e(S["email"])}">{e(S["email"])}</a></li>' if S.get("email") else ""
    return f"""</main>
<footer class="site-footer">
  <div class="wrap">
    {footer_brands()}
    <div class="footer-grid">
      <div>
        <a class="logo logo-footer" href="index.html"><img src="{PREFIX}assets/logo-full.png" alt="{e(S['name'])}" width="180" height="162"></a>
        <p style="margin-top:14px;max-width:34ch">{e(t(S, 'tagline'))} {e(T('footer_tag'))}</p>
      </div>
      <div><h4>{e(T('f_clinics'))}</h4><ul>{clinics}</ul></div>
      <div><h4>{e(T('f_concern'))}</h4><ul>{concerns}<li><a href="dokter.html">{e(T('f_doctors'))}</a></li></ul></div>
      <div><h4>{e(T('f_more'))}</h4><ul><li><a href="metode.html">{e(T('cy_name'))}</a></li><li><a href="edukasi.html">{e(T('f_edu'))}</a></li><li><a href="blog.html">{e(T('f_blog'))}</a></li><li><a href="harga-lengkap.html">{e(T('f_fp'))}</a></li><li><a href="analisis.html">{e(T('hero_btn2'))}</a></li></ul></div>
      <div><h4>{e(T('f_contact'))}</h4><ul>
        <li><a href="{WA}" target="_blank" rel="noopener">WhatsApp {e(S['whatsapp_display'])}</a><span class="small muted"><br>{e(t(S, 'whatsapp_hours'))}</span></li>
        {ig}{em}
      </ul></div>
    </div>
    <div class="footer-note">
      <span>© {datetime.date.today().year} {e(S['name'])}. {e(T('f_legal'))}</span>
      <span>{e(T('f_updated'))} {TODAY}</span>
    </div>
  </div>
</footer>
<div class="wa-bar">{wa_btn(T("generic_msg"), T("wa_bar"))}</div>
<script src="{av("site.js")}" defer></script>
</body>
</html>
"""

def cta_band():
    return f"""<section class="section"><div class="wrap">
  <div class="cta-band">
    <div><h2>{e(T('cta_h'))}</h2><p>{e(T('cta_p'))}</p></div>
    <div class="right">
      <div class="num">{e(S['whatsapp_display'])}</div>
      {wa_btn(T("generic_msg"), T("cta_btn"), "btn btn-primary")}
      <span class="small" style="color:rgba(255,247,243,.8)">{e(T('cta_hours'))} {e(t(S, 'whatsapp_hours'))}</span>
    </div>
  </div>
</div></section>
"""

# ---------------------------------------------------------------- structured data
def ld_clinic(c, nested=False):
    d = {"@type": "MedicalClinic", "name": c["name"], "telephone": "+" + S["whatsapp_number"],
         "address": {"@type": "PostalAddress", "streetAddress": c["address"], "addressLocality": c["area"], "addressCountry": "ID"},
         "hasMap": c["maps"], "openingHours": "Mo-Su 10:00-20:00", "url": page_url("klinik.html", L) + "#" + c["code"].lower()}
    if not nested: d["@context"] = "https://schema.org"
    return d
def ld_org():
    return {"@context": "https://schema.org", "@type": "MedicalBusiness", "name": S["name"], "url": S["url"], "telephone": "+" + S["whatsapp_number"],
            "description": t(S, "description"), "department": [ld_clinic(c, nested=True) for c in C["clinics"]]}
def ld_doctor(d):
    return {"@context": "https://schema.org", "@type": "Physician", "name": d["name"], "medicalSpecialty": "Dermatology",
            "worksFor": {"@type": "MedicalBusiness", "name": S["name"]},
            "workLocation": [{"@type": "MedicalClinic", "name": clinic(k)["name"]} for k in d["clinics"]]}
def ld_faq():
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": t(f, "q"), "acceptedAnswer": {"@type": "Answer", "text": t(f, "a")}} for f in C["faq"]]}
def ld_offers():
    items = [{"@type": "Offer", "name": o["name"], "category": t(con, "title"), "priceCurrency": "IDR", "price": o["single"],
              "description": t(o, "desc"), "url": page_url("menu.html", L) + "#" + con["code"].lower()} for con in C["concerns"] for o in con["offers"] if o.get("single")]
    return {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Menu Surface Skin Habit", "itemListElement": items}

# ---------------------------------------------------------------- blocks
def bs_hits(names):
    text = " | ".join(names).lower()
    return [b for b in C.get("bestsellers", {}).get("items", []) if any(m.lower() in text for m in b["match"])]

def bs_badge(names):
    hits = bs_hits(names)
    return f'<span class="bs-badge" title="{e(hits[0]["name"])}">{e(T("bs_badge"))}</span>' if hits else ""

def offer_block(con, o):
    inc = "".join(f"<li>{e(x)}</li>" for x in t(o, "includes"))
    msg = T("offer_msg", offer=o["name"], concern=t(con, "title"), klinik="{klinik}")
    return f"""<article class="offer" id="{e(slug(o['name']))}">
  <div>
    <div class="lv"><i></i> {e(o.get('level', '').capitalize())}{' · ' + e(T('needs_review')) if o.get('medical_review') and o.get('level') in ('correct', 'refine') and S.get('show_placeholders') else ''}</div>
    <h3>{e(o['name'])}{f' <small class="sig">{e(o["signature"])}</small>' if o.get('signature') and o['signature'] != o['name'] else ''}{bs_badge(o["includes"])}</h3>
    <ul class="inc">{inc}</ul>
    {brand_chips(t(o, "includes"))}
    <div class="meta"><span>⏱ {o['duration_min']} {e(T('min'))}</span><span>↻ {e(t(o, 'interval'))}</span></div>
    <p class="desc">{e(t(o, 'desc'))}</p>
  </div>
  <div class="prices">
    {f'<div class="price"><div class="k">{e(T("single"))}</div><div class="v">{rp(o["single"]) if o["single"] else ("Gratis" if L == "id" else "Free")}</div><div class="s">{e(T("one_session"))}</div></div>' if o.get("single") is not None else f'<div class="price"><div class="k">{e(T("single"))}</div><div class="v">{EM_DASH}</div><div class="s">{e(T("tx_consult"))}</div></div>'}
    {f'<div class="price"><div class="k">{e(T("pack3"))}</div><div class="v">{rp(o["pack3"])}</div><div class="s">{rp(o["pack3"]//3)} {e(T("per_session"))}</div></div>' if o.get("pack3") else f'<div class="price"><div class="k">{e(T("pack3"))}</div><div class="v">{EM_DASH}</div><div class="s">{e(T("tx_consult"))}</div></div>'}
    {f'<div class="price best"><div class="k">{e(T("pack6"))}</div><div class="v">{rp(o["pack6"])}</div><div class="s">{rp(o["pack6"]//6)} {e(T("per_session"))}</div></div>' if o.get("pack6") else f'<div class="price"><div class="k">{e(T("pack6"))}</div><div class="v">{EM_DASH}</div><div class="s">{e(T("tx_consult"))}</div></div>'}
  </div>
  <div class="cta">{wa_btn(msg, T("book_free"), "btn btn-primary btn-sm")}<span class="small">{e(T('doctor_confirms'))}</span></div>
</article>
"""

def concern_section(con):
    offers = "".join(offer_block(con, o) for o in con["offers"])
    tags = "".join(f'<span class="tag">{e(k)}</span>' for k in t(con, "keywords"))
    return f"""<section class="concern-block" id="{con['code'].lower()}">
  <span class="eyebrow">{e(con['name'])}</span>
  <h2>{e(t(con, 'title'))}</h2>
  <p class="intro">{e(t(con, 'intro'))}</p>
  <div class="tags" style="margin:0 0 20px">{tags}<a class="tag" href="{stream_file(con['code'])}" style="text-decoration:none">{e(T('home_streams_btn'))} \u2192</a></div>
  {offers}
</section>
"""

def side_blocks():
    pl = C["plan"]
    fv_items = "".join(f'<li><span><a href="{stream_file(con["code"])}">{e(o["name"])}</a><span class="f">{" + ".join(e(x) for x in t(o, "includes"))}</span></span><span class="p">{rp(o["single"]) if o.get("single") else ("Gratis" if L == "id" else "Free")}</span></li>' for con in C["concerns"] for o in con["offers"] if o.get("level") == "start")
    pl_inc = "".join(f"<li>{e(x)}</li>" for x in t(pl, "includes"))
    ad = "".join(f'<li><span><b>{e(a["name"])}</b> {MID_DOT} {e(t(a, "treatment"))}<span class="f">{e(t(a, "for"))}</span></span><span class="p">{rp(a["price"]) if a.get("price") else e(T("tx_consult"))}</span></li>' for a in C["addons"])
    return f"""<div class="side-blocks">
  <div class="card">
    <span class="eyebrow">{e(T('sc_eye'))}</span>
    <h3>{e(T('sc_h'))}</h3>
    <ul class="plist">{fv_items}</ul>
    <p class="small muted" style="margin-top:12px">{e(T('sc_note'))}</p>
    {wa_btn(T("fv_msg"), T("book_first"), "btn btn-ghost btn-sm")}
  </div>
  <div class="card">
    <span class="eyebrow">{e(T('monthly'))}</span>
    <h3>{e(pl['title'])}</h3>
    <div class="big-price">{rp(pl['price_month'])}<small> {e(T('per_month'))}</small></div>
    <ul class="check">{pl_inc}</ul>
    <p class="small muted">{e(t(pl, 'rules'))}</p>
    {wa_btn(T("plan_msg"), T("ask_plan"), "btn btn-ghost btn-sm")}
  </div>
  <div class="card">
    <span class="eyebrow">{e(T('extras'))}</span>
    <h3>{e(T('addons_h'))}</h3>
    <ul class="plist">{ad}</ul>
    <p class="small muted" style="margin-top:12px">{e(T('addons_note'))}</p>
  </div>
</div>"""

def doctor_cards(limit=None):
    docs = [d for d in C["doctors"] if d.get("publish")]
    docs = [d for d in docs if d.get("photo")] + [d for d in docs if not d.get("photo")]
    if limit: docs = docs[:limit]
    out = []
    for d in docs:
        initials = "".join(p[0] for p in d["name"].replace("dr.", "").split()[:2]).upper()
        where = " · ".join(clinic(k)["short"] for k in d["clinics"])
        tags = "".join(f'<span class="tag">{e(x)}</span>' for x in d["focus"])
        bio = f'<p class="small" style="margin:8px 0 0">{e(t(d, "bio"))}</p>' if d.get("bio") else ""
        creds = f'<ul class="creds">{"".join(f"<li>{e(x)}</li>" for x in t(d, "creds"))}</ul>' if d.get("creds") else ""
        ig = f'<a class="small ig" href="https://www.instagram.com/{e(d["instagram"])}/" target="_blank" rel="noopener">@{e(d["instagram"])}</a>' if d.get("instagram") else ""
        avatar = (f'<img class="avatar-img" src="{PREFIX}{e(d["photo"])}" alt="{e(d["name"])}" width="96" height="128" loading="lazy">'
                  if d.get("photo") else (f'<div class="avatar avatar-ph" title="{e(C["placeholders"]["doctor"])}"><span>{e(T("ph_label"))}</span></div>' if S.get("show_placeholders") else f'<div class="avatar" aria-hidden="true">{e(initials)}</div>'))
        out.append(f"""<div class="card doc">
  {avatar}
  <div><h3>{e(d['name'])}</h3><div class="role">{e(t(d, 'role'))} · {e(where)}</div><div class="tags">{tags}</div>{creds}{bio}{ig}</div>
</div>""")
    return "".join(out)

def clinic_cards():
    out = []
    for c in C["clinics"]:
        msg = T("clinic_msg", clinic=c["short"])
        out.append(f"""<div class="card clinic" id="{c['code'].lower()}">
  <div class="area">{e(t(c, 'area'))}</div>
  <h3>{e(c['name'])}</h3>
  <address>{e(c['address'])}</address>
  <div class="hours">{e(t(c, 'hours'))}</div>
  <div class="links">
    <a class="btn btn-ghost btn-sm" href="{e(c['maps'])}" target="_blank" rel="noopener">{e(T('open_maps'))}</a>
    {wa_btn(msg, T("book_here"), "btn btn-primary btn-sm", f'data-clinic-pick="{e(c["short"])}"')}
  </div>
</div>""")
    return "".join(out)

def faq_block():
    return '<div class="faq">' + "".join(f"<details><summary>{e(t(f, 'q'))}</summary><p>{e(t(f, 'a'))}</p></details>" for f in C["faq"]) + "</div>"

# ---------------------------------------------------------------- pages
def stream_file(code):
    st = C["streams"][code]
    return (st["slug_en"] if L == "en" else st["slug"]) + ".html"

def usp_block(compact=False):
    U = C["usp"]
    pts = "".join(f'<div class="usp"><h3>{e(t(x, "h"))}</h3><p>{e(t(x, "p"))}</p></div>' for x in U["points"])
    return f'''<section class="section usp-section" id="kenapa"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(t(U, "eyebrow"))}</span><h2>{e(t(U, "h"))}</h2><p>{e(t(U, "p"))}</p></div></div>
  <div class="usp-grid">{pts}</div>
</div></section>'''

def habit_strip(st):
    h = st.get("habit")
    if not h:
        return ""
    steps = "".join(f'<li>{e(x)}</li>' for x in t(h, "steps"))
    return f'''<section class="section" style="padding:0 0 8px"><div class="wrap">
  <div class="habit"><span class="eyebrow">{e(h["name"])}</span><ol class="habit-steps">{steps}</ol><span class="small muted">{e(C["brand"]["core"])}</span></div>
</div></section>'''

def next_door_block(con):
    nxt = [concern_of(k) for k in con.get("next", []) if concern_of(k) and C["streams"].get(k)]
    if not nxt: return ""
    chips = "".join(f'<a class="brand-chip" href="{stream_file(n["code"])}"><span>{e(n["name"])} · {e(t(n, "title"))}</span></a>' for n in nxt)
    return f'''<section class="section" style="padding-top:0"><div class="wrap"><div class="card"><span class="eyebrow">{e(T("next_door_h"))}</span><div class="brand-strip" style="margin-top:10px">{chips}</div></div></div></section>'''

def front_door_block():
    fd = C.get("front_door")
    if not fd: return ""
    return f'''<section class="section" style="padding-top:0"><div class="wrap"><div class="card" style="display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:space-between"><div><span class="eyebrow">{e(T("front_door_h"))}</span><h3 style="font-size:22px;margin:4px 0">{e(fd["name"])}</h3><p class="muted" style="margin:0">{e(t(fd, "desc"))}</p></div>{wa_btn(T("generic_msg"), T("book_free"), "btn btn-primary")}</div></div></section>'''

def page_stream(code):
    con = concern_of(code); st = C["streams"][code]
    for_you = "".join(f"<li>{e(x)}</li>" for x in t(st, "for_you"))
    steps = "".join(f'<li><div class="jw">{e(t(j, "when"))}</div><div><h3>{e(t(j, "title"))}</h3><p>{e(t(j, "body"))}</p></div></li>' for j in st["journey"])
    offers = "".join(offer_block(con, o) for o in con["offers"])
    promise = "".join(f"<li>{e(x)}</li>" for x in t(st, "promise"))
    nots = "".join(f"<li>{e(x)}</li>" for x in t(st, "not"))
    devs = [d for d in EDU["devices"] if code in d["concerns"]]
    chips = ""
    for d in devs:
        b = next((b for b in EDU["brands"] if b.get("device") == d["slug"]), None)
        logo_path = ROOT / "assets" / "brands" / (b.get("logo", "") if b else "")
        inner = (f'<img src="{PREFIX}assets/brands/{e(b["logo"])}" alt="{e(b["name"])}" loading="lazy">' if b and b.get("logo") and logo_path.exists() else f'<span>{e(d["name"])}</span>')
        chips += f'<a class="brand-chip" href="{dev_file(d)}" title="{e(d["name"])}">{inner}</a>'
    faq = '<div class="faq">' + "".join(f"<details><summary>{e(t(f, 'q'))}</summary><p>{e(t(f, 'a'))}</p></details>" for f in st["faq"]) + "</div>"
    msg = T("offer_msg", offer=t(st, "nav"), concern=t(con, "title"), klinik="{klinik}")
    devices_sec = (f'<section class="section" style="padding-top:0"><div class="wrap"><div class="section-head"><div><span class="eyebrow">{e(T("edu_eye"))}</span><h2>{e(T("st_devices"))}</h2></div>'
                   f'<a class="btn btn-ghost btn-sm" href="edukasi-brand.html">{e(T("br_strip_btn"))}</a></div><div class="brand-strip">{chips}</div></div></section>') if S.get("show_brand_mapping") else ""
    body = f'''<section class="hero"><div class="wrap">
  <div class="hero-card stream-hero">
    <div>
      <span class="eyebrow">{e(T("st_eye"))} \u00b7 {e(con["name"])}</span>
      <h1>{e(t(st, "h1"))}</h1>
      <p class="lead">{e(t(st, "lead"))}</p>
      <div class="hero-actions">{wa_btn(msg, T("st_start"), "btn btn-primary")}<a class="btn btn-ghost" href="analisis.html">{e(T("hero_btn2"))}</a></div>
    </div>
    {img_slot("stream_" + code, "hero-img")}
  </div>
</div></section>
<section class="section" style="padding:0 0 8px"><div class="wrap">{funnel_strip(code)}
  <div class="card for-you"><h3>{e(T("st_for"))}</h3><ul class="check">{for_you}</ul></div>
</div></section>
{habit_strip(st)}
<section class="section"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("st_eye"))}</span><h2>{e(T("st_journey"))}</h2></div></div>
  <div class="journey-split">{img_slot("treat_" + code, "treat-photo")}<ol class="journey">{steps}</ol></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="card helped"><span class="eyebrow">{e(t(C["proof"], "eyebrow"))}</span><h3>{e(T("st_helped"))}</h3><ul class="check">{"".join(f"<li>{e(x)}</li>" for x in t(st, "helped"))}</ul></div>
</div></section>
{results_block(code)}
{next_door_block(con)}
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="grid-2">
    <div class="card"><h3>{e(T("st_promise"))}</h3><ul class="check">{promise}</ul></div>
    <div class="card warn"><h3>{e(T("st_not"))}</h3><ul class="plist">{nots}</ul></div>
  </div>
</div></section>
<section class="section" style="padding-top:0" id="harga"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(con["name"])}</span><h2>{e(T("st_offers"))}</h2><p>{e(t(S, "consult_note"))}</p></div><a class="btn btn-ghost btn-sm" href="menu.html#{code.lower()}">{e(T("st_see_menu"))}</a></div>
  {offers}
  <p class="small muted">{e(t(S, "price_note"))}</p>
</div></section>
{stacks_block(door=code)}
{addons_strip()}
{devices_sec}
{usp_block()}
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("s4_eye"))}</span><h2>{e(T("st_doctors"))}</h2></div></div>
  <div class="grid-2">{doctor_cards(limit=4)}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("s6_eye"))}</span><h2>{e(T("st_faq"))}</h2></div></div>
  {faq}
</div></section>
{cta_band()}
'''
    title = T("t_st", nav=t(st, "nav"), name=S["name"])
    return head(title, t(st, "lead"), stream_file(code)) + header(stream_file(code)) + body + footer()

MID_DOT = "·"
PLUS_MINUS = "±"

def stack_card(x):
    inc = " + ".join(e(i) for i in t(x, "includes"))
    door = concern_of(x["door"]) if x.get("door") else None
    tag = e(door["name"]) if door else e(x.get("level", "").capitalize())
    dur = f'{PLUS_MINUS} {x["duration_min"]} {e(T("min"))}' if x.get("duration_min") else EM_DASH
    bits = [dur, f'{e(T("stk_for"))} {e(t(x, "for"))}'] + ([e(T("stk_downtime"))] if x.get("downtime") else [])
    price = rp(x["price"]) if x.get("price") else EM_DASH
    sub = e(T("stk_one")) if x.get("price") else e(T("tx_consult"))
    rev = f' <small class="sig">{e(T("needs_review"))}</small>' if x.get("medical_review") and S.get("show_placeholders") else ""
    msg = T("stk_msg", stack=x["name"], klinik="{klinik}")
    sep = f" {MID_DOT} "
    return f'''<article class="stack card" id="{e(slug(x["name"]))}">
  {img_slot("stack", "stack-photo")}
  <div class="stack-head"><span class="tag">{tag}</span><h3>{e(x["name"])}{rev}</h3></div>
  <p class="stack-inc">{inc}</p>
  {brand_chips(t(x, "includes"), 4)}
  <p class="small muted">{sep.join(bits)}</p>
  <div class="stack-price"><b>{price}</b><span class="small muted">{sub}</span></div>
  {wa_btn(msg, T("book_free"), "btn btn-ghost btn-sm")}
</article>'''

def stacks_block(door=None, compact=False):
    ST = C.get("stacks", {})
    items = [x for x in ST.get("items", []) if door is None or x.get("door") == door]
    if not items: return ""
    cards = "".join(stack_card(x) for x in items)
    if door:
        return f'''<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("stk_eye"))}</span><h2>{e(T("stk_door_h"))}</h2><p>{e(t(ST, "intro"))}</p></div><a class="btn btn-ghost btn-sm" href="menu.html#stack">{e(T("stk_btn"))}</a></div>
  <div class="stack-grid">{cards}</div>
</div></section>'''
    notes = "" if compact else f'''<div class="grid-2" style="margin-top:18px">
    <div class="card note"><h3>{e(T("stk_addons_h"))}</h3><p>{e(t(ST, "addons"))}</p></div>
    <div class="card note"><h3>{e(T("stk_before_h"))}</h3><p>{e(t(ST, "before"))}</p></div>
  </div>'''
    more = f'<a class="btn btn-ghost btn-sm" href="menu.html#stack">{e(T("stk_btn"))}</a>' if compact else ""
    extra = "" if compact else ph("stack")
    return f'''<section class="section" id="stack" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("stk_eye"))}</span><h2>{e(T("stk_h"))}</h2><p>{e(t(ST, "intro"))}</p></div>{more}</div>
  <div class="stack-grid">{cards}</div>{extra}
  {notes}
</div></section>'''

def addons_strip():
    AM = C.get("addons_meta", {})
    chips = "".join(f'<div class="addon"><b>{e(a["name"])}</b><span>{e(t(a, "treatment"))}</span><span class="small muted">{e(t(a, "for"))}</span><em>{rp(a["price"]) if a.get("price") else e(T("tx_consult"))}</em></div>' for a in C["addons"])
    return f'''<section class="section" id="addon" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("ad_eye"))}</span><h2>{e(T("ad_h"))}</h2><p>{e(t(AM, "intro"))}</p></div></div>
  <div class="addon-strip">{chips}</div>
  <p class="small muted" style="margin-top:12px"><b>{e(T("ad_after_h"))}.</b> {e(t(AM, "after"))}</p>
</div></section>'''

def results_block(code):
    R = C.get("results", {})
    rules = "".join(f"<li>{e(x)}</li>" for x in t(R, "rules"))
    if code in R.get("doors_excluded", []):
        body = f'<div class="card warn"><p>{e(T("res_tone"))}</p></div>'
    else:
        items = [x for x in R.get("items", []) if x.get("door") == code and x.get("publish") and x.get("consent_on_file") and x.get("doctor_signoff")]
        if items:
            pairs = ""
            sep = f" {MID_DOT} "
            for x in items:
                w = x.get("weeks", 12)
                cap = sep.join(v for v in [x.get("program"), clinic(x["clinic"])["short"] if x.get("clinic") else "", t(x, "caption")] if v)
                pairs += f'''<figure class="ba"><div class="ba-pair"><div><img src="{PREFIX}{e(x["before"])}" alt="{e(T("res_before"))}" loading="lazy"><span>{e(T("res_before"))}</span></div><div><img src="{PREFIX}{e(x["after"])}" alt="{e(T("res_after", w=w))}" loading="lazy"><span>{e(T("res_after", w=w))}</span></div></div><figcaption class="small muted">{e(cap)}</figcaption></figure>'''
            body = f'<div class="ba-grid">{pairs}</div>'
        else:
            pair = (f'<figure class="ba"><div class="ba-pair"><div class="ph ph-img ba-ph"><span class="small">{e(T("res_before"))}</span></div>'
                    f'<div class="ph ph-img ba-ph"><span class="small">{e(T("res_after", w=12))}</span></div></div>'
                    f'<figcaption class="small muted">{e(T("ph_label"))}: {e(t(R, "pair_spec"))}</figcaption></figure>')
            body = f'<p class="muted">{e(t(R, "empty"))}</p>' + (f'<div class="ba-grid">{pair * 3}</div>' if S.get("show_placeholders") else "")
    return f'''<section class="section" id="hasil" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("res_eye"))}</span><h2>{e(T("res_h"))}</h2><p>{e(t(R, "intro"))}</p></div></div>
  {body}
  <details class="small" style="margin-top:14px"><summary>{e(T("res_rules_h"))}</summary><ul class="plist">{rules}</ul></details>
</div></section>'''

def bestsellers_block():
    B = C.get("bestsellers", {})
    rows = ""
    for b in B.get("items", []):
        door = concern_of(b["door"]) if b.get("door") else None
        chip = f'<a class="tag" href="{stream_file(door["code"])}">{e(door["name"])}</a>' if door else ""
        rows += f'<li><span class="bs-rank">{b["rank"]}</span><div><b>{e(b["name"])}</b><span class="small muted">{e(T("bs_where"))}: <a href="{e(b["href"])}">{e(t(b, "where"))}</a></span></div>{chip}</li>'
    return f'''<section class="section" id="terlaris" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("bs_eye"))}</span><h2>{e(T("bs_h"))}</h2><p>{e(t(B, "basis"))}</p></div></div>
  <ol class="bs-list">{rows}</ol>
</div></section>'''

def page_pricelist():
    PL = C.get("pricelist", {})
    fams = ""
    for f in EDU["treatment_families"]:
        rows = ""
        for x in [x for x in EDU["treatments"] if x["family"] == f["code"]]:
            price = rp(x["price"]) if x["price"] else T("tx_consult")
            rows += (f'<tr><td><b>{e(x["name"])}</b>{bs_badge([x["name"]])}<br><span class="small muted">{e(t(x, "for"))}</span>{brand_chips([x["name"], x["brand"]], 3)}</td>'
                     f'<td>{e(T("by_doctor") if x["performed_by"] == "doctor" else T("by_therapist"))}</td>'
                     f'<td>{x["duration_min"]} {e(T("min"))}</td><td class="p">{e(price)}</td></tr>')
        fams += f'<tr class="fam"><th colspan="4">{e(t(f, "name"))}</th></tr>{rows}'
    prog = ""
    for con in C["concerns"]:
        for o in con["offers"]:
            single = rp(o["single"]) if o.get("single") else ("Gratis" if L == "id" else "Free") if o.get("single") == 0 else EM_DASH
            prog += (f'<tr><td><b><a href="menu.html#{e(slug(o["name"]))}">{e(o["name"])}</a></b>{bs_badge(o["includes"])}<br><span class="small muted">{" + ".join(e(x) for x in t(o, "includes"))}</span>{brand_chips(t(o, "includes"), 4)}</td>'
                     f'<td>{e(con["name"])}</td><td class="p">{single}</td><td class="p">{rp(o["pack3"]) if o.get("pack3") else EM_DASH}</td><td class="p">{rp(o["pack6"]) if o.get("pack6") else EM_DASH}</td></tr>')
    stacks = "".join(f'<tr><td><b>{e(x["name"])}</b><br><span class="small muted">{" + ".join(e(i) for i in t(x, "includes"))}</span></td><td>{e(concern_of(x["door"])["name"]) if x.get("door") else e(x.get("level", "").capitalize())}</td><td class="p">{rp(x["price"]) if x.get("price") else e(T("tx_consult"))}</td></tr>' for x in C.get("stacks", {}).get("items", []))
    addons = "".join(f'<tr><td><b>{e(a["name"])}</b> {MID_DOT} {e(t(a, "treatment"))}<br><span class="small muted">{e(t(a, "for"))}</span></td><td class="p">{rp(a["price"]) if a.get("price") else e(T("tx_consult"))}</td></tr>' for a in C["addons"])
    pl = C["plan"]
    tabs = "".join(f'<a href="#{k}">{e(T(v))}</a>' for k, v in (("program", "fp_programs"), ("satuan", "fp_singles"), ("stack", "fp_stacks"), ("addon", "fp_addons"), ("plan", "fp_plan")))
    body = f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T("fp_eye"))}</span>
  <h1>{e(T("fp_h1"))}</h1>
  <p class="lead">{e(t(PL, "intro"))}</p>
  <div class="menu-tabs" style="margin-top:22px">{tabs}<a href="menu.html">{e(T("menu_eye"))} →</a></div>
</div></section>
<section class="section" id="program" style="padding-top:12px"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("fp_eye"))}</span><h2>{e(T("fp_programs"))}</h2></div><a class="btn btn-ghost btn-sm" href="menu.html">{e(T("menu_eye"))}</a></div>
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("tm_what"))}</th><th>{e(T("f_concern"))}</th><th>{e(T("single"))}</th><th>{e(T("pack3"))}</th><th>{e(T("pack6"))}</th></tr></thead><tbody>{prog}</tbody></table></div>
</div></section>
<section class="section" id="satuan" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("fp_eye"))}</span><h2>{e(T("fp_singles"))}</h2></div><a class="btn btn-ghost btn-sm" href="edukasi-treatment.html">{e(T("tx_h1"))}</a></div>
  <div class="tx-wrap"><table class="tx-table fp"><thead><tr><th>{e(T("tm_what"))}</th><th>{e(T("tx_by"))}</th><th>{e(T("tx_dur"))}</th><th>{e(T("tx_price"))}</th></tr></thead><tbody>{fams}</tbody></table></div>
  <p class="small muted" style="margin-top:12px">{e(t(PL, "rx_note"))}</p>
</div></section>
<section class="section" id="stack" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("stk_eye"))}</span><h2>{e(T("fp_stacks"))}</h2></div></div>
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("tm_what"))}</th><th>{e(T("f_concern"))}</th><th>{e(T("stk_one"))}</th></tr></thead><tbody>{stacks}</tbody></table></div>
</div></section>
<section class="section" id="addon" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("ad_eye"))}</span><h2>{e(T("fp_addons"))}</h2></div></div>
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("tm_what"))}</th><th>{e(T("ad_fixed"))}</th></tr></thead><tbody>{addons}</tbody></table></div>
</div></section>
<section class="section" id="plan" style="padding-top:0"><div class="wrap">
  <div class="card"><span class="eyebrow">{e(T("monthly"))}</span><h3>{e(pl["title"])}</h3><div class="big-price">{rp(pl["price_month"])}<small> {e(T("per_month"))}</small></div><ul class="check">{"".join(f"<li>{e(x)}</li>" for x in t(pl, "includes"))}</ul><p class="small muted">{e(t(pl, "rules"))}</p>{wa_btn(T("plan_msg"), T("ask_plan"), "btn btn-ghost btn-sm")}</div>
  <p class="small muted" style="margin-top:14px">{e(t(S, "price_note"))}</p>
</div></section>
{cta_band()}
'''
    return head(T("t_fp", name=S["name"]), T("d_fp"), "harga-lengkap.html", [ld_offers()]) + header("menu.html", "harga-lengkap.html") + body + footer()

def space_fig(x, cls=""):
    klass = "sp" + (" " + cls if cls else "")
    return f'<figure class="{klass}"><img src="{PREFIX}{e(x["src"])}" alt="{e(t(x, "alt"))}" loading="lazy"><figcaption class="small">{e(t(x, "alt"))}</figcaption></figure>'

def spaces_block(limit=8):
    SPx = C.get("spaces", {}); items = SPx.get("items", [])[:limit]
    if not items: return ""
    figs = "".join(space_fig(x, "feature" if x.get("feature") else "") for x in items)
    return f'''<section class="section" id="ruang" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("sp_eye"))}</span><h2>{e(T("sp_h"))}</h2><p>{e(t(SPx, "intro"))}</p></div><a class="btn btn-ghost btn-sm" href="klinik.html">{e(T("sp_btn"))}</a></div>
  <div class="spaces-grid">{figs}</div>
</div></section>'''

def clinic_photos(code):
    items = [x for x in C.get("spaces", {}).get("items", []) if x.get("clinic") == code]
    if not items: return img_slot("clinic_" + code) or ph("clinic")
    return f'<div class="clinic-photos">{"".join(space_fig(x) for x in items[:4])}</div>'

def img_slot(key, cls=""):
    x = C.get("images", {}).get(key)
    if not x: return ""
    klass = "img-slot" + (" " + cls if cls else "")
    ratio = x.get("ratio", "4/3")
    if x.get("src"):
        return f'<figure class="{klass}" style="aspect-ratio:{ratio}"><img src="{PREFIX}{e(x["src"])}" alt="{e(t(x, "alt"))}" loading="lazy"></figure>'
    if S.get("show_placeholders"):
        return f'<div class="{klass} ph ph-img" style="aspect-ratio:{ratio}"><span class="small">{e(T("ph_label"))}</span><p class="small">{e(t(x, "spec"))}</p></div>'
    return ""

def start_blocks():
    pl = C["plan"]
    rows = "".join(f'<li><span><a href="{stream_file(con["code"])}">{e(o["name"])}</a><span class="f">{" + ".join(e(x) for x in t(o, "includes"))}</span></span><span class="p">{rp(o["single"]) if o.get("single") else ("Gratis" if L == "id" else "Free")}</span></li>' for con in C["concerns"] for o in con["offers"] if o.get("level") == "start")
    pl_inc = "".join(f"<li>{e(x)}</li>" for x in t(pl, "includes"))
    return f'''<div class="grid-2 start-blocks">
  <div class="card">
    <span class="eyebrow">{e(T('sc_eye'))}</span>
    <h3>{e(T('sc_h'))}</h3>
    <ul class="plist">{rows}</ul>
    <p class="small muted" style="margin-top:12px">{e(T('sc_note'))}</p>
    {wa_btn(T("fv_msg"), T("book_first"), "btn btn-primary btn-sm")}
  </div>
  <div class="card">
    <span class="eyebrow">{e(T('monthly'))}</span>
    <h3>{e(pl['title'])}</h3>
    <div class="big-price">{rp(pl['price_month'])}<small> {e(T('per_month'))}</small></div>
    <ul class="check">{pl_inc}</ul>
    <p class="small muted">{e(t(pl, 'rules'))}</p>
    {wa_btn(T("plan_msg"), T("ask_plan"), "btn btn-ghost btn-sm")}
  </div>
</div>'''

def brands_for(texts, limit=6):
    text = " | ".join(texts).lower()
    out = []
    for b in EDU["brands"]:
        if any(k in text for k in b.get("keywords", [])) and b not in out:
            out.append(b)
    return out[:limit]

def brand_mini(b):
    logo_path = ROOT / "assets" / "brands" / b.get("logo", "")
    inner = (f'<img src="{PREFIX}assets/brands/{e(b["logo"])}" alt="{e(b["name"])}" loading="lazy">'
             if b.get("logo") and logo_path.exists() else f'<span>{e(b["name"])}</span>')
    return f'<a class="brand-mini" href="edukasi-brand.html" title="{e(b["name"])}">{inner}</a>'

def brand_chips(texts, limit=6):
    if not S.get("show_brand_mapping"): return ""
    bs = brands_for(texts, limit)
    if not bs: return ""
    return f'<div class="brand-minis" aria-label="{e(T("br_used"))}">{"".join(brand_mini(b) for b in bs)}</div>'

def footer_brands():
    bs = [b for b in EDU["brands"] if b.get("logo") and (ROOT / "assets" / "brands" / b["logo"]).exists()]
    if not bs: return ""
    return f'<div class="footer-brands"><span class="small muted">{e(T("br_strip_h"))}</span><div class="brand-minis">{"".join(brand_mini(b) for b in bs)}</div></div>'

def cycle_svg(compact=False, standalone=False):
    # The Skin Habit Cycle diagram: five stations on a ring, the doctor at the centre, Refine as a branch from Review.
    import math
    steps = T("cy_steps"); refine = T("cy_refine"); centre = T("cy_centre")
    W, H, cx, cy, R = 820, 600, 410, 300, 200
    ACC, INK, SOFT, PANEL, BG = "#9B5A47", "#1E1A18", "#6B5F5A", "#F4E3DD", "#FBF7F4"
    pts = []
    for i in range(5):
        a = math.radians(-90 + i * 72)
        pts.append((cx + R * math.cos(a), cy + R * math.sin(a)))
    ring = f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="6 8" opacity=".55"/>'
    arrows = ""
    for i in range(5):
        a0 = math.radians(-90 + i * 72 + 22); a1 = math.radians(-90 + (i + 1) * 72 - 22)
        x0, y0 = cx + R * math.cos(a0), cy + R * math.sin(a0); x1, y1 = cx + R * math.cos(a1), cy + R * math.sin(a1)
        arrows += f'<path d="M{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{ACC}" stroke-width="3" marker-end="url(#cy-arrow)"/>'
    nodes = ""
    for i, (name, line, when, body) in enumerate(steps):
        x, y = pts[i]
        anchor = "middle"
        lx, ly = x, y + 66
        if i == 1: anchor, lx, ly = "start", x + 54, y + 4
        if i == 2: anchor, lx, ly = "start", x + 46, y + 30
        if i == 3: anchor, lx, ly = "end", x - 46, y + 30
        if i == 4: anchor, lx, ly = "end", x - 54, y + 4
        if i == 0: ly = y - 60
        nodes += (f'<g><circle cx="{x:.1f}" cy="{y:.1f}" r="40" fill="{"#fff" if i else ACC}" stroke="{ACC}" stroke-width="3"/>'
                  f'<text x="{x:.1f}" y="{y + 7:.1f}" text-anchor="middle" font-size="22" font-weight="700" fill="{ACC if i else "#fff"}">{i + 1}</text>'
                  f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" font-size="20" font-weight="700" fill="{INK}">{e(name.upper())}</text>'
                  f'<text x="{lx:.1f}" y="{ly + 22:.1f}" text-anchor="{anchor}" font-size="13.5" fill="{SOFT}">{e(when)}</text></g>')
    rx, ry = pts[3]
    refine_g = (f'<path d="M{rx - 30:.1f},{ry + 30:.1f} L{rx - 95:.1f},{ry + 95:.1f}" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="5 6" marker-end="url(#cy-arrow)"/>'
                f'<rect x="{rx - 215:.1f}" y="{ry + 96:.1f}" width="118" height="40" rx="20" fill="{PANEL}" stroke="{ACC}" stroke-width="2"/>'
                f'<text x="{rx - 156:.1f}" y="{ry + 122:.1f}" text-anchor="middle" font-size="16" font-weight="700" fill="{ACC}">{e(refine[0].upper())}</text>')
    centre_g = (f'<circle cx="{cx}" cy="{cy}" r="78" fill="{PANEL}"/>'
                f'<text x="{cx}" y="{cy - 2}" text-anchor="middle" font-size="26" font-weight="700" fill="{ACC}">{e(centre[0])}</text>'
                f'<text x="{cx}" y="{cy + 24}" text-anchor="middle" font-size="14" fill="{SOFT}">{e(centre[1])}</text>')
    title = (f'<text x="{cx}" y="{H - 22}" text-anchor="middle" font-size="15" font-weight="700" letter-spacing="2" fill="{ACC}">{e(T("cy_name").upper())}{e(T("cy_tm"))} · SURFACE SKIN HABIT</text>') if standalone else ""
    bg = f'<rect width="{W}" height="{H}" fill="{BG}"/>' if standalone else ""
    font = 'font-family="Gotham, Montserrat, Helvetica, Arial, sans-serif"'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{e(T("cy_name"))}" class="cycle-svg{" compact" if compact else ""}" {font}>'
            f'<defs><marker id="cy-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{ACC}"/></marker></defs>'
            f'{bg}{ring}{arrows}{centre_g}{refine_g}{nodes}{title}</svg>')

def cycle_block(compact=False):
    btn = f'<a class="btn btn-ghost btn-sm" href="metode.html">{e(T("cy_more"))}</a>' if compact else ""
    return f'''<section class="section" id="siklus" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("cy_eye"))}</span><h2>{e(T("cy_name"))}<sup class="tm">{e(T("cy_tm"))}</sup> · {e(T("cy_h"))}</h2><p>{e(T("cy_p"))}</p></div>{btn}</div>
  <div class="cycle-wrap">{cycle_svg(compact)}</div>
</div></section>'''

def page_cycle():
    steps = ""
    for i, (name, line, when, body) in enumerate(T("cy_steps"), 1):
        steps += f'<li><div class="jw">{e(when)}</div><div><h3>{e(name)} · {e(line)}</h3><p>{e(body)}</p></div></li>'
    refine = T("cy_refine")
    body = f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T("cy_eye"))}</span>
  <h1>{e(T("cy_name"))}<sup class="tm">{e(T("cy_tm"))}</sup></h1>
  <p class="lead">{e(T("cy_p"))}</p>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap"><div class="cycle-wrap big">{cycle_svg()}</div></div></section>
{venn_block()}
<section class="section" style="padding-top:0"><div class="wrap">
  <ol class="journey">{steps}</ol>
  <div class="card note" style="margin-top:18px"><h3>{e(refine[0])}</h3><p>{e(refine[1])}</p></div>
</div></section>
{funnel_strip()}
{cta_band()}
'''
    return head(T("t_cy", name=S["name"]), T("d_cy"), "metode.html") + header("index.html#concern", "metode.html") + body + footer()

def venn_svg(standalone=False):
    # The Skin Habit mark: three overlapping sets (Doctor, Plan, Habit), multiply-blended so the overlaps read on their own.
    ACC, INK, SOFT, BG = "#9B5A47", "#1E1A18", "#6B5F5A", "#FBF7F4"
    TINTS = ["#C98B79", "#E7B9A9", "#B7A39A"]
    W, H, cx, cy, r, d = 820, 640, 410, 340, 182, 104
    sets = T("vn_sets"); ov = T("vn_overlaps"); centre = T("vn_centre")
    circles = [(cx, cy - d), (cx - d * 1.02, cy + d * 0.62), (cx + d * 1.02, cy + d * 0.62)]
    # set names sit inside their own circle, away from the overlaps
    names = [(cx, cy - d - r * 0.52), (cx - d * 1.02 - r * 0.28, cy + d * 0.62 + r * 0.6), (cx + d * 1.02 + r * 0.28, cy + d * 0.62 + r * 0.6)]
    ovpos = [(cx - d * 0.95, cy - d * 0.3), (cx + d * 0.95, cy - d * 0.3), (cx, cy + d * 1.08)]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="Skin Habit" class="venn-svg" font-family="Gotham, Montserrat, Helvetica, Arial, sans-serif">']
    if standalone: out.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    out.append('<g style="mix-blend-mode:multiply">')
    for (x, y), tint in zip(circles, TINTS):
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="{tint}" fill-opacity=".82"/>')
    out.append('</g>')
    for (n, sub), (x, y) in zip(sets, names):
        out.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-size="26" font-weight="800" letter-spacing="3" fill="{INK}">{e(n.upper())}</text>'
                   f'<text x="{x:.0f}" y="{y + 24:.0f}" text-anchor="middle" font-size="14" font-weight="600" fill="{INK}" fill-opacity=".72">{e(sub)}</text>')
    for (n, sub), (x, y) in zip(ov, ovpos):
        out.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-size="14" font-weight="800" letter-spacing="2" fill="{INK}">{e(n.upper())}</text>'
                   f'<text x="{x:.0f}" y="{y + 17:.0f}" text-anchor="middle" font-size="12.5" font-weight="600" fill="{INK}" fill-opacity=".75">{e(sub)}</text>')
    out.append(f'<circle cx="{cx}" cy="{cy + 10}" r="52" fill="{ACC}" stroke="{BG}" stroke-width="5"/>'
               f'<text x="{cx}" y="{cy + 6}" text-anchor="middle" font-size="15" font-weight="800" letter-spacing="3" fill="#fff">{e(centre[0])}</text>'
               f'<text x="{cx}" y="{cy + 26}" text-anchor="middle" font-size="15" font-weight="800" letter-spacing="3" fill="#fff">{e(centre[1])}</text>')
    if standalone: out.append(f'<text x="{cx}" y="{H - 22}" text-anchor="middle" font-size="14" font-weight="700" letter-spacing="3" fill="{ACC}">SKIN HABIT\u2122 \u00b7 SURFACE SKIN HABIT</text>')
    out.append('</svg>')
    return "".join(out)

def venn_block():
    return f'''<section class="section" id="skin-habit" style="padding-top:0"><div class="wrap">
  <div class="venn-split">
    <div class="venn-wrap">{venn_svg()}</div>
    <div><span class="eyebrow">{e(T("cy_eye"))}</span><h2>Skin Habit<sup class="tm">{e(T("cy_tm"))}</sup> · {e(T("vn_h"))}</h2><p>{e(T("vn_p"))}</p><a class="btn btn-ghost btn-sm" href="metode.html">{e(T("cy_more"))}</a></div>
  </div>
</div></section>'''

def proof_block():
    P = C["proof"]
    stats = "".join(f'<div class="stat"><div class="n">{e(t(x, "n"))}</div><div class="l">{e(t(x, "l"))}</div></div>' for x in P["stats"])
    return f'''<section class="section proof" id="sejak-2014" style="padding-top:0"><div class="wrap">
  <div class="proof-card">
    <div class="section-head" style="margin-bottom:18px"><div><span class="eyebrow">{e(t(P, "eyebrow"))}</span><h2>{e(t(P, "h"))}</h2><p>{e(t(P, "p"))}</p></div></div>
    <div class="stats">{stats}</div>
  </div>
</div></section>'''

def ph(key, cls="ph"):
    if not S.get("show_placeholders"):
        return ""
    return f'<div class="{cls}"><span class="small">{e(T("ph_label"))}</span><p class="small">{e(C["placeholders"][key])}</p></div>'

def funnel_strip(active=None):
    chips = ""
    for con in C["concerns"]:
        st = C["streams"].get(con["code"])
        if not st: continue
        cur = ' aria-current="page"' if st and active == con["code"] else ""
        chips += f'<a href="{stream_file(con["code"])}"{cur}><b>{e(con["name"])}</b><span>{e(t(con, "title"))}</span></a>'
    return f'<nav class="funnel-strip" aria-label="{e(T("funnels_h"))}">{chips}</nav>'

def instagram_block():
    ig = C["social"]["instagram"]; h = ig.get("handle", "")
    if not h: return ""
    posts = ig.get("posts", [])
    if posts:
        tiles = "".join(f'<blockquote class="instagram-media" data-instgrm-permalink="{e(u)}" data-instgrm-version="14"><a href="{e(u)}" target="_blank" rel="noopener">{e(u)}</a></blockquote>' for u in posts[:6])
        script = '<script async src="https://www.instagram.com/embed.js"></script>'
    else:
        tiles = "".join(f'<div class="ig-ph"><span>{e(T("ph_label"))}</span><p class="small">{e(T("ig_ph"))}</p></div>' for _ in range(3)) if S.get("show_placeholders") else ""
        script = ""
    return f'''<section class="section" id="instagram" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">Instagram</span><h2>{e(T("ig_h"))}</h2></div><a class="btn btn-ghost btn-sm" href="https://www.instagram.com/{e(h)}/" target="_blank" rel="noopener">{e(T("ig_follow", h=h))}</a></div>
  <div class="ig-grid">{tiles}</div>{script}
</div></section>'''

def google_reviews_block():
    rows = ""
    for c in C["clinics"]:
        write = f'<a class="btn btn-primary btn-sm" href="https://search.google.com/local/writereview?placeid={e(c["google_place_id"])}" target="_blank" rel="noopener">{e(T("gr_write"))}</a>' if c.get("google_place_id") else ""
        rows += f'''<div class="gr"><div><b>{e(c["name"])}</b><div class="small muted">{e(t(c, "area"))}</div></div><div class="gr-stars" aria-hidden="true">\u2605\u2605\u2605\u2605\u2605</div><div class="tags-btn"><a class="btn btn-ghost btn-sm" href="{e(c.get("google_reviews", c["maps"]))}" target="_blank" rel="noopener">{e(T("gr_read"))}</a>{write}</div></div>'''
    return f'<div class="card" style="margin-top:18px"><h3>{e(T("gr_h"))}</h3><p class="small muted">{e(T("tm_google_p"))}</p><div class="gr-list">{rows}</div>{ph("review", "ph ph-inline")}</div>'

def testimonials_block():
    TM = C.get("testimonials", {})
    items = [x for x in TM.get("items", []) if x.get("publish")]
    cards = ""
    for x in items:
        vid = f'<div class="video"><iframe src="{e(x["video_url"])}" title="{e(x["name"])}" loading="lazy" allowfullscreen></iframe></div>' if x.get("video_url") else ""
        who = " \u00b7 ".join(v for v in [x.get("name"), clinic(x["clinic"])["short"] if x.get("clinic") else "", x.get("treatment")] if v)
        cards += f'<figure class="card quote">{vid}<blockquote>{e(t(x, "quote"))}</blockquote><figcaption class="small muted">{e(who)}</figcaption></figure>'
    links = "".join(f'<a class="btn btn-ghost btn-sm" href="{e(c["google_reviews"])}" target="_blank" rel="noopener">{e(c["short"])}</a>' for c in C["clinics"] if c.get("google_reviews"))
    quotes = f'<div class="grid-3">{cards}</div>' if cards else ""
    return f'''<section class="section" id="testimoni" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("tm_eye"))}</span><h2>{e(T("tm_h"))}</h2><p>{e(t(TM, "intro"))}</p></div></div>
  {quotes}
  {google_reviews_block()}
</div></section>'''

def brand_strip():
    chips = ""
    for b in EDU["brands"][:10]:
        logo_path = ROOT / "assets" / "brands" / b.get("logo", "")
        inner = (f'<img src="{PREFIX}assets/brands/{e(b["logo"])}" alt="{e(b["name"])}" loading="lazy">'
                 if b.get("logo") and logo_path.exists() else f'<span>{e(b["name"])}</span>')
        chips += f'<a class="brand-chip" href="edukasi-brand.html">{inner}</a>'
    return f'''<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("edu_eye"))}</span><h2>{e(T("br_strip_h"))}</h2><p>{e(T("br_strip_p"))}</p></div><a class="btn btn-ghost btn-sm" href="edukasi-brand.html">{e(T("br_strip_btn"))}</a></div>
  <div class="brand-strip">{chips}</div>
</div></section>'''

def page_index():
    concern_cards = "".join(f"""<a class="card card-link concern-card" href="{stream_file(c['code'])}">
  <div class="code">{e(c['name'])}</div>
  <h3>{e(t(c, 'title'))}</h3>
  <p>{e(t(c, 'intro'))}</p>
  <div class="from">{e(T('from'))} <b>{rp(min_single(c))}</b> {e(T('per_session_long'))} · {e(T('levels_short'))}</div>
  <span class="small edu-more">{e(T('home_streams_btn'))} →</span>
</a>""" for c in C["concerns"])
    trust = "".join(f"<span><b>{e(a)}</b> {e(b)}</span>" for a, b in T("trust"))
    body = f"""<section class="hero"><div class="wrap">
  <div class="hero-card hero-photo">
    <div>
      <span class="eyebrow">{e(T('hero_eyebrow', n=len(C['clinics'])))}</span>
      <h1>{e(T('hero_h1'))}</h1>
      <p class="lead">{e(T('hero_lead'))}</p>
      <div class="hero-actions">
        {wa_btn(T("generic_msg"), T("book_free"), "btn btn-primary")}
        <a class="btn btn-ghost" href="analisis.html">{e(T('hero_btn2'))}</a>
      </div>
      <div class="trust">{trust}</div>
    </div>
    {img_slot("hero", "hero-img")}
  </div>
</div></section>

{venn_block()}
<section class="section" id="concern" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T('s1_eye'))}</span><h2>{e(T('s1_h'))}</h2><p>{e(T('s1_p'))}</p></div><a class="btn btn-ghost btn-sm" href="menu.html">{e(T('s1_btn'))}</a></div>
  {funnel_strip()}
  <div class="grid-3">{concern_cards}</div>
</div></section>

<section class="section" id="mulai" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T('s3_eye'))}</span><h2>{e(T('s3_h'))}</h2><p>{e(T('s3_p'))}</p></div></div>
  {start_blocks()}
</div></section>
{brand_strip()}

<section class="section" id="dokter" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T('s4_eye'))}</span><h2>{e(T('s4_h'))}</h2><p>{e(T('s4_p'))}</p></div><a class="btn btn-ghost btn-sm" href="dokter.html">{e(T('s4_btn'))}</a></div>
  <div class="doctor-split">{img_slot("doctor_consult", "doctor-photo")}<div class="grid-2">{doctor_cards(limit=2)}</div></div>
</div></section>

{testimonials_block()}
{instagram_block()}
{cta_band()}
"""
    return head(T("t_index", name=S["name"]), t(S, "description"), "index.html", [ld_org(), ld_faq()]) + header("index.html") + body + footer()

def page_menu():
    tabs = "".join(f'<a href="#{c["code"].lower()}">{e(c["name"])} · {e(t(c, "title"))}</a>' for c in C["concerns"])
    body = f"""<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T('menu_eye'))}</span>
  <h1>{e(T('menu_h1'))}</h1>
  <p class="lead">{e(t(S, 'consult_note'))} {e(T('menu_lead_tail'))}</p>
  <div class="menu-tabs" style="margin-top:22px">{tabs}<a href="#terlaris">{e(T('bs_tab'))}</a><a href="#stack">{e(T('stk_tab'))}</a><a href="#pertama">{e(T('menu_tab_extra'))}</a><a href="harga-lengkap.html">{e(T('fp_tab'))} →</a></div>
</div></section>
{front_door_block()}
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="levels" style="margin-bottom:28px">{"".join(f'<div class="level"><div class="lv">{e(l["name"])}</div><p>{e(t(l, "blurb"))}</p></div>' for l in C["levels"])}</div>
  {"".join(concern_section(c) for c in C["concerns"])}
  <p class="small muted" style="margin-top:8px">{e(t(S, 'price_note'))} {e(T('menu_other'))}</p>
</div></section>
{bestsellers_block()}
{stacks_block()}
{addons_strip()}
<section class="section" id="pertama" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T('menu_s2_eye'))}</span><h2>{e(T('menu_s2_h'))}</h2></div></div>
  {side_blocks()}
</div></section>
{cta_band()}
"""
    return head(T("t_menu", name=S["name"]), T("d_menu"), "menu.html", [ld_offers()]) + header("menu.html") + body + footer()

def page_doctors():
    body = f"""<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T('doc_eye'))}</span>
  <h1>{e(T('doc_h1'))}</h1>
  <p class="lead">{e(T('doc_lead'))}</p>
</div></section>
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="grid-2">{doctor_cards()}</div>
  <p class="small muted" style="margin-top:18px">{e(T('doc_note'))}</p>
</div></section>
{cta_band()}
"""
    ld = [ld_doctor(d) for d in C["doctors"] if d.get("publish")]
    return head(T("t_doc", name=S["name"]), T("d_doc"), "dokter.html", ld) + header("dokter.html") + body + footer()

def clinic_detail(c):
    q = urllib.parse.quote(c["address"])
    devs = ""
    for d in EDU["devices"]:
        if c["code"] not in d["clinics"]: continue
        b = next((b for b in EDU["brands"] if b.get("device") == d["slug"]), None)
        lp = ROOT / "assets" / "brands" / (b.get("logo", "") if b else "")
        inner = f'<img src="{PREFIX}assets/brands/{e(b["logo"])}" alt="{e(b["name"])}" loading="lazy">' if b and b.get("logo") and lp.exists() else f'<span>{e(d["name"])}</span>'
        devs += f'<li><a class="brand-mini" href="{dev_file(d)}" title="{e(d["name"])}">{inner}</a></li>'
    docs = ", ".join(d["name"] for d in C["doctors"] if d.get("publish") and c["code"] in d["clinics"])
    msg = T("clinic_msg", clinic=c["short"])
    return f'''<article class="card clinic clinic-full" id="{c['code'].lower()}">
  <div class="clinic-grid">
    <div>
      <div class="area">{e(t(c, 'area'))}</div>
      <h3>{e(c['name'])}</h3>
      <address>{e(c['address'])}</address>
      <div class="hours">{e(t(c, 'hours'))}</div>
      <div class="links">
        <a class="btn btn-ghost btn-sm" href="{e(c['maps'])}" target="_blank" rel="noopener">{e(T('open_maps'))}</a>
        <a class="btn btn-ghost btn-sm" href="{e(c.get('google_reviews', c['maps']))}" target="_blank" rel="noopener">{e(T('cl_reviews'))}</a>
        {wa_btn(msg, T("book_here"), "btn btn-primary btn-sm", f'data-clinic-pick="{e(c["short"])}"')}
      </div>
      {f'<p class="small" style="margin:16px 0 6px"><b>{e(T("cl_doctors"))}</b><br>{e(docs)}</p>' if docs else ""}
      <p class="small" style="margin:14px 0 6px"><b>{e(T("cl_devices"))}</b></p>
      <ul class="brand-minis tags">{devs}</ul>
      {clinic_photos(c["code"])}
    </div>
    <div class="map"><iframe src="https://www.google.com/maps?q={q}&output=embed" title="{e(T('cl_map'))}: {e(c['name'])}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </div>
</article>'''

def page_clinics():
    body = f"""<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T('cl_eye'))}</span>
  <h1>{e(T('cl_h1'))}</h1>
  <p class="lead">{e(T('cl_lead', hours=t(S, 'whatsapp_hours')))}</p>
</div></section>
<section class="section" style="padding-top:12px"><div class="wrap">
  {"".join(clinic_detail(c) for c in C["clinics"])}
</div></section>
{cta_band()}
"""
    return head(T("t_cl", name=S["name"]), T("d_cl"), "klinik.html", [ld_clinic(c) for c in C["clinics"]]) + header("klinik.html") + body + footer()

def localise_assessment():
    """Resolve the assessment to the current language so analisis.js stays language-agnostic."""
    A = json.loads(json.dumps(C["assessment"]))
    def fix(d, keys):
        for k in keys:
            if k in d: d[k] = t(d, k)
    fix(A, ["title", "subtitle", "disclaimer"]); fix(A["scan"], ["title", "help"])
    for st in A.get("skin_types", {}).values(): fix(st, ["name", "desc", "care"])
    for b in A["blocks"]:
        fix(b, ["title", "intro"])
        for q in b["questions"]:
            fix(q, ["text", "placeholder", "flag"])
            for o in q.get("options", []): fix(o, ["label"])
            for lst in q.get("options_by_concern", {}).values():
                for o in lst: fix(o, ["label"])
    concerns = []
    for con in C["concerns"]:
        c2 = {"code": con["code"], "name": con["name"], "title": t(con, "title"), "intro": t(con, "intro"), "offers": []}
        for o in con["offers"]:
            c2["offers"].append({"name": o["name"], "level": o.get("level"), "includes": t(o, "includes"), "duration_min": o["duration_min"],
                                 "interval": t(o, "interval"), "single": o["single"], "pack3": o["pack3"], "pack6": o["pack6"]})
        concerns.append(c2)
    return A, concerns

def page_assessment():
    A, concerns = localise_assessment()
    embed = json.dumps({"assessment": A, "concerns": concerns, "site": {"whatsapp_number": S["whatsapp_number"]}, "ui": T("aq_js")}, ensure_ascii=False).replace("</", "<\\/")
    static = ""
    for b in A["blocks"]:
        static += f'<h3>{e(T("aq_block"))} {e(b["code"])} · {e(b["title"])}</h3><ol>' + "".join(f"<li>{e(q['text'])}</li>" for q in b["questions"]) + "</ol>"
    scan_js = f'<script src="{av("scan-adapter.js")}" defer></script>' if A["scan"].get("enabled") else ""
    cards = "".join(f'<div class="card"><h3>{e(h)}</h3><p>{e(p)}</p></div>' for h, p in T("aq_cards"))
    body = f"""<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T('aq_eye'))}</span>
  <h1>{e(A['title'])}</h1>
  <p class="lead">{e(A['subtitle'])}</p>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <div class="aq-card">
    <div id="analisis" class="aq">
      <noscript><p class="aq-help">{e(T('aq_noscript'))}</p>{static}{wa_btn(T("generic_msg"), T("wa_bar"), "btn btn-primary")}</noscript>
    </div>
  </div>
  <div class="grid-3" style="margin-top:28px">{cards}</div>
</div></section>
{cta_band()}
<script type="application/json" id="ssh-data">{embed}</script>
{scan_js}
<script src="{av("analisis.js")}" defer></script>
"""
    return head(T("t_aq", name=S["name"]), T("d_aq"), "analisis.html") + header("analisis.html") + body + footer()

# ---------------------------------------------------------------- education
EDU = C["education"]
EN_DASH = "\u2013"
EM_DASH = "\u2014"

def devices(family=None):
    return [d for d in EDU["devices"] if family is None or d["family"] == family]
def dev_file(d):
    return "edukasi-" + d["slug"] + ".html"
def by_label(d):
    return T("by_doctor") if d["performed_by"] == "doctor" else T("by_therapist")
def dev_clinics(d, short=True):
    if len(d["clinics"]) == len(C["clinics"]):
        return T("fam_all_clinics")
    return ", ".join(clinic(k)["short"] for k in d["clinics"])
def concern_of(code):
    return next((c for c in C["concerns"] if c["code"] == code), None)

def fitz_table(d):
    leg = t(EDU, "fitz_legend")
    rows = ""
    for band in ("I-II", "III-IV", "V-VI"):
        v = d["fitz"][band]
        mark = {"ok": "\u25cf", "caution": "\u26a0", "avoid": "\u2014"}[v]
        rows += (f'<tr class="f-{v}"><th scope="row">{e(band.replace("-", EN_DASH))}</th>'
                 f'<td><span class="f-mark" aria-hidden="true">{mark}</span> {e(leg[v])}</td></tr>')
    return f'<table class="fitz"><caption class="sr-only">{e(T("dev_fitz"))}</caption><tbody>{rows}</tbody></table>'

def device_card(d):
    tags = "".join(f'<li class="tag">{e(x)}</li>' for x in t(d, "treats")[:3])
    return f'''<a class="card card-link edu-card" href="{dev_file(d)}">
  {img_slot("device_" + d["slug"], "card-photo")}
  <span class="eyebrow">{e(t(d, "brand"))}</span>
  <h3>{e(d["name"])}</h3>
  <p class="muted">{e(t(d, "how"))}</p>
  <ul class="tags">{tags}</ul>
  <p class="small edu-meta">{e(d["duration_min"])} {e(T("min"))} \u00b7 {e(t(d, "interval"))} \u00b7 {e(by_label(d))}</p>
  <span class="small edu-more">{e(T("edu_learn"))} \u2192</span>
</a>'''

def ld_edu_hub():
    items = [{"@type": "ListItem", "position": i + 1, "name": d["name"], "url": page_url(dev_file(d), L)}
             for i, d in enumerate(EDU["devices"])]
    return [{"@context": "https://schema.org", "@type": "MedicalWebPage", "name": T("t_edu", name=S["name"]),
             "description": T("d_edu"), "url": page_url("edukasi.html", L), "lastReviewed": TODAY,
             "audience": {"@type": "Patient"}, "about": {"@type": "MedicalBusiness", "name": S["name"]}},
            {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items},
            {"@context": "https://schema.org", "@type": "DefinedTermSet", "name": T("edu_gloss_h"),
             "hasDefinedTerm": [{"@type": "DefinedTerm", "name": t(g, "term"), "description": t(g, "def")} for g in EDU["glossary"]]}]

def ld_device(d):
    return [{"@context": "https://schema.org", "@type": "MedicalWebPage",
             "name": T("t_dev", dev=d["name"], name=S["name"]), "url": page_url(dev_file(d), L),
             "lastReviewed": TODAY, "audience": {"@type": "Patient"},
             "about": {"@type": "MedicalProcedure", "name": d["name"], "howPerformed": t(d, "how"),
                       "bodyLocation": "Skin", "preparation": t(d, "fitz_note"),
                       "followup": " ".join(t(d, "aftercare"))}},
            {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": T("edu_eye"), "item": page_url("edukasi.html", L)},
                {"@type": "ListItem", "position": 2, "name": d["name"]}]}]

def page_education():
    fams = ""
    for f in EDU["families"]:
        ds = devices(f["code"])
        if not ds:
            continue
        fams += f'''<section class="section" style="padding-top:8px"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("edu_fam_h"))}</span><h2>{e(t(f, "name"))}</h2><p>{e(t(f, "blurb"))}</p></div></div>
  <div class="grid-3">{"".join(device_card(d) for d in ds)}</div>
</div></section>'''
    gloss = "".join(f'''<div class="gloss"><dt>{e(t(g, "term"))}</dt><dd>{e(t(g, "def"))}</dd></div>''' for g in EDU["glossary"])
    hubs = "".join(f'<a class="edu-hub" href="{h}"><span class="eyebrow">{e(T("edu_eye"))}</span><h3>{e(n)}</h3><p>{e(d)}</p></a>' for h, n, d in T("edu_hubs"))
    body = f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T("edu_eye"))}</span>
  <h1>{e(T("edu_h1"))}</h1>
  <p class="lead">{e(t(EDU, "intro"))}</p>
</div></section>
<section class="section" style="padding-top:8px"><div class="wrap">
  <div class="edu-hubs">{hubs}</div>
</div></section>
<section class="section" style="padding-bottom:0"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("edu_eye"))}</span><h2>{e(T("edu_devices_h"))}</h2><p>{e(T("edu_devices_p"))}</p></div></div>
</div></section>
{fams}
<section class="section"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(T("edu_gloss_eye"))}</span><h2>{e(T("edu_gloss_h"))}</h2><p>{e(T("edu_gloss_p"))}</p></div></div>
  <dl class="gloss-list">{gloss}</dl>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <aside class="card note"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</div></section>
{cta_band()}
'''
    return head(T("t_edu", name=S["name"]), T("d_edu"), "edukasi.html", ld_edu_hub()) + header("edukasi.html") + body + footer()

def page_device(d):
    treats = "".join(f"<li>{e(x)}</li>" for x in t(d, "treats"))
    avoid = "".join(f"<li>{e(x)}</li>" for x in t(d, "avoid_if"))
    after = "".join(f"<li>{e(x)}</li>" for x in t(d, "aftercare"))
    paras = "".join(f"<p>{e(x)}</p>" for x in t(d, "detail").split("\n\n"))
    rel = ""
    for code in d["concerns"]:
        con = concern_of(code)
        if con:
            rel += f'''<a class="btn btn-ghost btn-sm" href="menu.html#{con["code"].lower()}">{e(con["name"])} \u00b7 {e(t(con, "title"))}</a>'''
    spec = [(T("dev_type"), t(d, "type")), (T("dev_dur"), f'{d["duration_min"]} {T("min")}'),
            (T("dev_int"), t(d, "interval")), (T("dev_down"), t(d, "downtime")),
            (T("dev_feel"), t(d, "sensation")), (T("dev_by"), by_label(d)), (T("dev_at"), dev_clinics(d))]
    spec_rows = "".join(f'<div class="spec"><dt>{e(k)}</dt><dd>{e(v)}</dd></div>' for k, v in spec)
    body = f'''<section class="page-hero dev-head"><div class="wrap dev-hero">
  <div>
  <a class="small edu-back" href="edukasi.html">\u2190 {e(T("edu_back"))}</a>
  <span class="eyebrow">{e(t(d, "brand"))}</span>
  <h1>{e(d["name"])}</h1>
  <p class="lead">{e(t(d, "how"))}</p>
  </div>
  {img_slot("device_" + d["slug"], "device-photo")}
</div></section>
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="grid-2 dev-grid">
    <div>
      <h2>{e(T("dev_detail"))}</h2>
      {paras}
      <h2 style="margin-top:28px">{e(T("dev_treats"))}</h2>
      <ul class="check">{treats}</ul>
      {f'<h2 style="margin-top:28px">{e(T("dev_related"))}</h2><div class="tags-btn">{rel}</div>' if rel else ""}
    </div>
    <aside>
      <div class="card">
        <h3>{e(T("dev_spec"))}</h3>
        <dl class="spec-list">{spec_rows}</dl>
      </div>
      <div class="card" style="margin-top:16px">
        <h3>{e(T("dev_fitz"))}</h3>
        {fitz_table(d)}
        <p class="small muted">{e(t(d, "fitz_note"))}</p>
      </div>
    </aside>
  </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="grid-2">
    <div class="card warn"><h3>{e(T("dev_avoid"))}</h3><ul class="plist">{avoid}</ul></div>
    <div class="card"><h3>{e(T("dev_after"))}</h3><ul class="plist">{after}</ul></div>
  </div>
  <aside class="card note" style="margin-top:16px"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</div></section>
{cta_band()}
'''
    desc = T("d_dev", how=t(d, "how"), dur=d["duration_min"], interval=t(d, "interval"), by=by_label(d), clinics=dev_clinics(d))
    return (head(T("t_dev", dev=d["name"], name=S["name"]), desc, dev_file(d), ld_device(d))
            + header("edukasi.html", dev_file(d)) + body + footer())

def edu_subnav(active):
    links = ""
    for h, n, _ in T("edu_hubs"):
        cur = ' aria-current="page"' if h == active else ""
        links += f'<a href="{h}"{cur}>{e(n)}</a>'
    return f'<div class="edu-subnav"><a href="edukasi.html">{e(T("edu_all"))}</a>{links}</div>'

def edu_head(title, eyebrow, lead, active):
    return f'''<section class="page-hero"><div class="wrap">
  <a class="small edu-back" href="edukasi.html">\u2190 {e(T("edu_back"))}</a>
  <span class="eyebrow">{e(eyebrow)}</span>
  <h1>{e(title)}</h1>
  <p class="lead">{e(lead)}</p>
  {edu_subnav(active)}
</div></section>'''

def dev_by_slug(slug):
    return next((d for d in EDU["devices"] if d["slug"] == slug), None)

def page_treatments():
    fams = ""
    for f in EDU["treatment_families"]:
        rows = ""
        for x in [x for x in EDU["treatments"] if x["family"] == f["code"]]:
            dev = dev_by_slug(x["device"]) if x["device"] else None
            link = f'<br><a class="small" href="{dev_file(dev)}">{e(T("tx_device_link"))} \u2192</a>' if dev else ""
            price = rp(x["price"]) if x["price"] else T("tx_consult")
            note = f'<br><span class="small muted">{e(t(x, "note"))}</span>' if x.get("note") else ""
            brand_td = f'<td>{e(x["brand"])}{link}</td>' if S.get("show_brand_mapping") else ""
            rows += (f'<tr><td><b>{e(x["name"])}</b>{bs_badge([x["name"]])}{note}</td><td>{e(t(x, "for"))}</td>{brand_td}'
                     f'<td>{e(T("by_doctor") if x["performed_by"] == "doctor" else T("by_therapist"))}</td>'
                     f'<td>{x["duration_min"]} {e(T("min"))}<br><span class="small muted">{e(t(x, "interval"))}</span></td><td class="p">{e(price)}</td></tr>')
        fams += f'''<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(t(f, "name"))}</span><h2>{e(t(f, "name"))}</h2><p>{e(t(f, "blurb"))}</p></div></div>
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("tm_what"))}</th><th>{e(T("tx_for"))}</th>{f'<th>{e(T("tx_brand"))}</th>' if S.get("show_brand_mapping") else ""}<th>{e(T("tx_by"))}</th><th>{e(T("tx_dur"))} · {e(T("tx_int"))}</th><th>{e(T("tx_price"))}</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>'''
    body = edu_head(T("tx_h1"), T("tx_eye"), t(EDU, "treatments_intro"), "edukasi-treatment.html") + fams + f'''
<section class="section" style="padding-top:0"><div class="wrap">
  <p class="small muted">{e(t(S, "price_note"))}</p>
  <aside class="card note" style="margin-top:16px"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</div></section>
{cta_band()}
'''
    return head(T("t_tx", name=S["name"]), T("d_tx"), "edukasi-treatment.html") + header("edukasi.html", "edukasi-treatment.html") + body + footer()

def brand_card(b):
    dev = dev_by_slug(b["device"]) if b.get("device") else None
    link = f'<a class="btn btn-ghost btn-sm" href="{dev_file(dev)}">{e(T("tx_device_link"))}</a>' if dev else ""
    site = f'<a class="btn btn-ghost btn-sm" href="{e(b["site"])}" target="_blank" rel="noopener">{e(T("br_site"))} \u2197</a>' if b.get("site") else ""
    used = "".join(f'<li class="tag">{e(u)}</li>' for u in b["used_in"])
    logo_path = ROOT / "assets" / "brands" / b.get("logo", "")
    logo = (f'<img class="brand-logo" src="{PREFIX}assets/brands/{e(b["logo"])}" alt="{e(b["name"])}" loading="lazy">'
            if b.get("logo") and logo_path.exists() else "")
    regs = "".join(f'<li><a href="{e(r["url"])}" target="_blank" rel="noopener">{e(t(r, "label"))}</a></li>' if r.get("url") else f'<li>{e(t(r, "label"))}</li>' for r in b.get("regulatory", []))
    if b.get("kemenkes_akl"):
        regs += f'<li>Izin edar Kemenkes {e(b["kemenkes_akl"])}</li>'
    reg_block = f'<p class="small" style="margin:10px 0 4px"><b>{e(T("br_reg"))}</b></p><ul class="reg-list">{regs}</ul>' if regs else ""
    at = f'<p class="small muted" style="margin:8px 0 0">{e(T("br_at"))}: {e(dev_clinics(dev))}</p>' if dev else ""
    return f'''<div class="card brand-card">
  {logo}
  <span class="eyebrow">{e(t(b, "kind"))}</span>
  <h3>{e(b["name"])}</h3>
  <p class="small muted" style="margin:0 0 4px">{e(T("br_maker"))}: {e(b["maker"])}</p>
  {f'<p class="small muted" style="margin:0 0 8px">{e(T("br_origin"))}: {e(t(b, "origin"))}</p>' if t(b, "origin") not in ("", EN_DASH, EM_DASH) else ""}
  <p>{e(t(b, "what"))}</p>
  {reg_block}
  {f'<p class="small" style="margin:10px 0 6px"><b>{e(T("br_used"))}</b></p><ul class="tags">{used}</ul>' if S.get("show_brand_mapping") else ""}
  {at}
  {f'<div class="tags-btn" style="margin-top:14px">{link}{site}</div>' if (link or site) else ""}
</div>'''

def page_brands():
    sections = ""
    for cat in EDU["brand_categories"]:
        cards = ""
        for b in [b for b in EDU["brands"] if b.get("category") == cat["code"]]:
            cards += brand_card(b)
        if cards:
            sections += f'''<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="section-head"><div><span class="eyebrow">{e(t(cat, "name"))}</span><h2>{e(t(cat, "name"))}</h2><p>{e(t(cat, "blurb"))}</p></div></div>
  <div class="grid-3">{cards}</div>
</div></section>'''
    cards = sections
    # device × clinic matrix
    head_cells = "".join(f'<th>{e(c["short"])}</th>' for c in C["clinics"])
    rows = ""
    for d in EDU["devices"]:
        DOT, DASH = "\u25cf", "\u2014"
        cells = "".join(f'<td class="mx">{DOT if c["code"] in d["clinics"] else DASH}</td>' for c in C["clinics"])
        rows += f'<tr><td><a href="{dev_file(d)}">{e(d["name"])}</a><br><span class="small muted">{e(t(d, "brand"))}</span></td>{cells}</tr>'
    matrix = f'''<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><h2>{e(t(EDU, "brands_matrix_h"))}</h2></div></div>
  <div class="tx-wrap"><table class="tx-table matrix"><thead><tr><th>{e(T("br_matrix_dev"))}</th>{head_cells}</tr></thead><tbody>{rows}</tbody></table></div>
  <p class="small muted" style="margin-top:12px">{e(t(EDU, "brands_reg_note"))}</p>
</div></section>'''
    body = edu_head(T("br_h1"), T("tx_eye"), t(EDU, "brands_intro"), "edukasi-brand.html") + f'''
{cards}
<section class="section" style="padding-top:0"><div class="wrap">
  <p class="small muted" style="margin-bottom:12px">{e(t(EDU, "brands_reg_note"))}</p>
  <aside class="card note"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</div></section>
{cta_band()}
'''
    return head(T("t_br", name=S["name"]), T("d_br"), "edukasi-brand.html") + header("edukasi.html", "edukasi-brand.html") + body + footer()

def page_combinations():
    CB = EDU["combinations"]
    rules = "".join(f'<div class="rule"><h3>{e(t(r, "h"))}</h3><p>{e(t(r, "p"))}</p></div>' for r in CB["rules"])
    seqs = ""
    for q in CB["sequences"]:
        steps = "".join(f'<li><span>{e(a)}</span><span class="m">{m} {e(T("min"))}</span></li>' for a, m in t(q, "steps"))
        tl = "".join(f'<li><b>{e(w)}</b><span>{e(x)}</span></li>' for w, x in t(q, "timeline"))
        offers = "".join(f'<a class="tag" href="menu.html#{slug(o)}" style="text-decoration:none">{e(o)}</a>' for o in q["offers"])
        seqs += f'''<article class="seq">
  <h3>{e(t(q, "name"))}</h3>
  <div class="meta">\u23f1 {q["total_min"]} {e(T("min"))} {e(T("cb_total"))} \u00b7 \u21bb {e(t(q, "interval"))} \u00b7 {e(T("cb_offers"))}: <span class="tags" style="display:inline-flex;margin:0 0 0 6px">{offers}</span></div>
  <div class="seq-grid">
    <div><h4 class="eyebrow">{e(T("cb_steps"))}</h4><ol class="steps-list">{steps}</ol></div>
    <div><h4 class="eyebrow">{e(T("cb_timeline"))}</h4><ul class="tl">{tl}</ul></div>
  </div>
</article>'''
    nots = "".join(f'<tr><td><b>{e(t(n, "a"))}</b></td><td>{e(t(n, "b"))}</td><td>{e(t(n, "why"))}</td></tr>' for n in CB["not_together"])
    body = edu_head(T("cb_h1"), T("tx_eye"), t(CB, "intro"), "edukasi-kombinasi.html") + f'''
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="section-head"><div><h2>{e(T("cb_rules_h"))}</h2></div></div>
  <div class="grid-3">{rules}</div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><h2>{e(T("cb_seq_h"))}</h2><p>{e(T("cb_seq_p"))}</p></div></div>
  {seqs}
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="section-head"><div><h2>{e(T("cb_not_h"))}</h2></div></div>
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("cb_not_a"))}</th><th>{e(T("cb_not_b"))}</th><th>{e(T("cb_not_why"))}</th></tr></thead><tbody>{nots}</tbody></table></div>
  <aside class="card note" style="margin-top:24px"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</div></section>
{cta_band()}
'''
    return head(T("t_cb", name=S["name"]), T("d_cb"), "edukasi-kombinasi.html") + header("edukasi.html", "edukasi-kombinasi.html") + body + footer()

def page_timing():
    TM = EDU["timing"]
    rows = "".join(f'<tr><td><b>{e(t(r, "what"))}</b></td><td>{e(t(r, "interval"))}</td><td>{e(t(r, "series"))}</td><td>{e(t(r, "why"))}</td></tr>' for r in TM["intervals"])
    courses = "".join(f'<li><b>{e(t(r, "k"))}</b><span>{e(t(r, "v"))}</span></li>' for r in TM["courses"])
    waits = "".join(f'<li><b>{e(t(r, "k"))}</b><span>{e(t(r, "v"))}</span></li>' for r in TM["waits"])
    rebook = "".join(f'<li><b>{e(t(r, "k"))}</b><span>{e(t(r, "v"))}</span></li>' for r in TM["rebook"])
    body = edu_head(T("tm_h1"), T("tx_eye"), t(TM, "intro"), "edukasi-waktu.html") + f'''
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="section-head"><div><h2>{e(T("tm_int_h"))}</h2></div></div>
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("tm_what"))}</th><th>{e(T("tm_int"))}</th><th>{e(T("tm_series"))}</th><th>{e(T("tm_why"))}</th></tr></thead><tbody>{rows}</tbody></table></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="grid-2">
    <div class="card"><h3>{e(T("tm_course_h"))}</h3><ul class="kv">{courses}</ul></div>
    <div class="card"><h3>{e(T("tm_rebook_h"))}</h3><p class="small muted">{e(T("tm_rebook_p"))}</p><ul class="kv">{rebook}</ul></div>
  </div>
  <div class="card warn" style="margin-top:18px"><h3>{e(T("tm_wait_h"))}</h3><ul class="kv">{waits}</ul></div>
  <aside class="card note" style="margin-top:18px"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</div></section>
{cta_band()}
'''
    return head(T("t_tm", name=S["name"]), T("d_tm"), "edukasi-waktu.html") + header("edukasi.html", "edukasi-waktu.html") + body + footer()

def post_file(x):
    return "blog-" + (x["slug_en"] if L == "en" else x["slug"]) + ".html"

def page_blog():
    cards = ""
    for x in C["posts"]:
        cards += f'''<a class="card card-link" href="{post_file(x)}"><span class="eyebrow">{e(x["date"])}</span><h3>{e(t(x, "title"))}</h3><p class="muted">{e(t(x, "summary"))}</p><span class="small edu-more">{e(T("blog_read"))} \u2192</span></a>'''
    body = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">{e(T("blog_h"))}</span><h1>{e(T("blog_h"))}</h1><p class="lead">{e(T("blog_lead"))}</p></div></section>
<section class="section" style="padding-top:12px"><div class="wrap"><div class="grid-2">{cards}</div></div></section>
{cta_band()}
'''
    return head(T("t_blog", name=S["name"]), T("d_blog"), "blog.html") + header("blog.html") + body + footer()

def page_post(x):
    paras = "".join(f"<p>{e(par)}</p>" for par in t(x, "body"))
    con = concern_of(x["cta_stream"])
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": t(x, "title"), "datePublished": x["date"], "author": {"@type": "Organization", "name": S["name"]}, "publisher": {"@type": "Organization", "name": S["name"]}, "description": t(x, "summary"), "inLanguage": L}
    body = f'''<section class="page-hero"><div class="wrap"><a class="small edu-back" href="blog.html">\u2190 {e(T("blog_back"))}</a><span class="eyebrow">{e(x["date"])}</span><h1>{e(t(x, "title"))}</h1><p class="lead">{e(t(x, "summary"))}</p></div></section>
<section class="section" style="padding-top:12px"><div class="wrap"><article class="post">{paras}
  <div class="tags-btn" style="margin-top:22px"><a class="btn btn-primary" href="{stream_file(x["cta_stream"])}">{e(T("blog_cta"))}: {e(con["name"])}</a><a class="btn btn-ghost" href="analisis.html">{e(T("hero_btn2"))}</a></div>
  <aside class="card note" style="margin-top:22px"><h3>{e(T("edu_disclaimer_h"))}</h3><p class="muted">{e(t(EDU, "disclaimer"))}</p></aside>
</article></div></section>
{cta_band()}
'''
    return head(t(x, "title") + " \u00b7 " + S["name"], t(x, "summary"), post_file(x), [ld]) + header("blog.html", post_file(x)) + body + footer()

def page_cs():
    CS = C["cs"]
    items = ""
    for i, it in enumerate(CS["items"]):
        url = BASE + "/" + it["link"]
        items += f'''<details class="cs-item" {"open" if i == 0 else ""}><summary>{e(it["q"])}</summary>
  <p>{e(it["a"])}</p>
  <div class="cs-row"><a class="btn btn-ghost btn-sm" href="{e(it["link"])}">{e(T("cs_link"))} \u2192</a><code class="small">{e(url)}</code><button type="button" class="btn btn-ghost btn-sm copy" data-copy="{e(url)}">{e(T("cs_copy"))}</button></div>
  <div class="tpl"><span class="eyebrow">{e(T("cs_tpl"))}</span><p>{e(it["tpl"])}</p><button type="button" class="btn btn-ghost btn-sm copy" data-copy="{e(it["tpl"])}">{e(T("cs_copy"))}</button></div>
</details>'''
    rules = "".join(f"<li>{e(r)}</li>" for r in CS["rules"])
    body = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">Internal</span><h1>{e(CS["title"])}</h1><p class="lead">{e(CS["intro"])}</p></div></section>
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="card warn"><h3>Aturan singkat</h3><ul class="plist">{rules}</ul></div>
  <div class="cs-list" style="margin-top:18px">{items}</div>
</div></section>
<script>document.querySelectorAll(".copy").forEach(function(b){{b.addEventListener("click",function(){{var v=b.getAttribute("data-copy");(navigator.clipboard&&navigator.clipboard.writeText?navigator.clipboard.writeText(v):Promise.reject()).then(function(){{b.textContent="{e(T("cs_copied"))}";setTimeout(function(){{b.textContent="{e(T("cs_copy"))}"}},1500)}}).catch(function(){{window.prompt("Salin:",v)}})}})}});</script>
'''
    h = head(CS["title"] + " \u00b7 " + S["name"], CS["intro"], "cs.html").replace("</head>", '<meta name="robots" content="noindex,nofollow">\n</head>')
    return h + header("") + body + footer()

def page_seo():
    SEO = C["seo"]
    rows = "".join(f'<tr><td><b>{e(r["kw"])}</b></td><td>{e(r["intent"])}</td><td><a href="{e(r["page"])}">{e(r["page"])}</a></td><td>{e(r["status"])}</td></tr>' for r in SEO["map"])
    rules = "".join(f"<li>{e(r)}</li>" for r in SEO["rules"])
    body = f'''<section class="page-hero"><div class="wrap"><span class="eyebrow">Internal</span><h1>{e(SEO["title"])}</h1><p class="lead">{e(SEO["intro"])}</p></div></section>
<section class="section" style="padding-top:12px"><div class="wrap">
  <div class="tx-wrap"><table class="tx-table"><thead><tr><th>{e(T("seo_kw"))}</th><th>{e(T("seo_intent"))}</th><th>{e(T("seo_page"))}</th><th>{e(T("seo_status"))}</th></tr></thead><tbody>{rows}</tbody></table></div>
  <div class="card" style="margin-top:18px"><h3>Aturan</h3><ul class="plist">{rules}</ul></div>
</div></section>
'''
    h = head(SEO["title"] + " \u00b7 " + S["name"], SEO["intro"], "seo.html").replace("</head>", '<meta name="robots" content="noindex,nofollow">\n</head>')
    return h + header("") + body + footer()

def page_404():
    rootp = "/en/" if L == "en" else "/"
    links = "".join(f'<li><a href="{rootp + ("" if h == "index.html" else h)}">{e(label)}</a></li>' for h, label in T("nav"))
    body = f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{e(T("e404_eye"))}</span>
  <h1>{e(T("e404_h"))}</h1>
  <p class="lead">{e(T("e404_p"))}</p>
  <div class="hero-actions"><a class="btn btn-primary" href="{rootp}">{e(T("e404_home"))}</a></div>
  <ul class="plist" style="margin-top:22px">{links}</ul>
</div></section>
{cta_band()}
'''
    h = head(T("t_404", name=S["name"]), T("e404_p"), "404.html").replace(
        "</head>", '<meta name="robots" content="noindex">\n</head>')
    return h + header("") + body + footer()

def _stream_pages():
    return {code: (lambda code=code: page_stream(code)) for code in C["streams"]}
PAGES = {"index.html": page_index, "menu.html": page_menu, "metode.html": page_cycle, "harga-lengkap.html": page_pricelist, "edukasi.html": page_education,
         "edukasi-treatment.html": page_treatments, "edukasi-brand.html": page_brands, "edukasi-kombinasi.html": page_combinations, "edukasi-waktu.html": page_timing,
         "analisis.html": page_assessment, "dokter.html": page_doctors, "klinik.html": page_clinics}
for _d in EDU["devices"]:
    PAGES[dev_file(_d)] = (lambda dd: lambda: page_device(dd))(_d)
PAGES["404.html"] = page_404
INDEXABLE = [k for k in PAGES if k != "404.html"]

# ---------------------------------------------------------------- claims lint
# Indonesia regulates whitening and skin-lightening claims in aesthetic advertising. BANNED fails
# the build; REVIEW prints a warning so a human decides (product names like "Brightening Peel" are
# proper nouns, but a descriptive promise is not).
BANNED = ["memutihkan", "pemutih", "memutihkan kulit", "whitening", "whiten", "bleaching", "bleach the skin",
          "lebih putih", "kulit putih", "skin lightening", "lightening", "lighten your skin", "glutathione"]
REVIEW = ["mencerahkan", "pencerah", "lebih cerah", "brightening", "brighten", "before and after",
          "sebelum dan sesudah", "before & after", "dijamin", "guaranteed", "permanen", "permanent"]

def lint_claims(pages):
    import re as _re
    banned_hits, review_hits = [], []
    for name, content in pages:
        text = _re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", content, flags=_re.S | _re.I)
        text = html.unescape(_re.sub(r"<[^>]+>", " ", text))
        for tier, words, sink in (("BANNED", BANNED, banned_hits), ("REVIEW", REVIEW, review_hits)):
            for w in words:
                for m in _re.finditer(r"\b" + _re.escape(w) + r"\b", text, _re.I):
                    a, b = max(0, m.start() - 60), min(len(text), m.end() + 60)
                    sink.append((name, w, " ".join(text[a:b].split())))
    return banned_hits, review_hits


def sitemap():
    urls = ""
    for p in list(INDEXABLE) + [st["slug"] + ".html" for st in C["streams"].values()] + ["blog.html"] + ["blog-" + x["slug"] + ".html" for x in C["posts"]]:
        for lang in ("id", "en"):
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l2}" href="{page_url(alt_path(p, l2), l2)}"/>' for l2 in ("id", "en"))
            urls += f"<url><loc>{page_url(alt_path(p, lang), lang)}</loc><lastmod>{TODAY}</lastmod>{alts}</url>"
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">{urls}</urlset>\n'

def main():
    global L, PREFIX
    rendered = []
    for lang, outdir, prefix in (("id", ROOT, ""), ("en", ROOT / "en", "../")):
        L, PREFIX = lang, prefix
        outdir.mkdir(exist_ok=True)
        pages = dict(PAGES)
        for code in C["streams"]:
            pages[stream_file(code)] = (lambda code=code: page_stream(code))
        pages["blog.html"] = page_blog
        for x in C["posts"]:
            pages[post_file(x)] = (lambda x=x: page_post(x))
        pages["cs.html"] = page_cs
        pages["seo.html"] = page_seo
        for name, fn in pages.items():
            rendered.append((outdir / name, fn()))

    banned, review = lint_claims([(f.relative_to(ROOT), c) for f, c in rendered])
    if banned:
        print("\nCLAIMS LINT FAILED \u2014 nothing written.\n")
        for name, w, ctx in banned:
            print(f'  {name}: "{w}"\n    \u2026{ctx}\u2026')
        print("\nWhitening and skin-lightening claims are regulated in Indonesia. Rewrite the copy")
        print("around pigment and evenness, then build again.")
        raise SystemExit(1)

    for f, content in rendered:
        f.write_text(content, encoding="utf-8")
        print("wrote", f.relative_to(ROOT), f"({len(content):,} bytes)")

    if review:
        seen = set()
        print(f"\n{len(review)} phrase(s) to review by a human:")
        for name, w, ctx in review:
            if (name, w) in seen:
                continue
            seen.add((name, w))
            print(f'  {name}: "{w}"\n    \u2026{ctx}\u2026')
    for lang in ("id", "en"):
        L, PREFIX = lang, ""
        (ROOT / "assets" / f"skin-habit-cycle-{lang}.svg").write_text(cycle_svg(standalone=True), encoding="utf-8")
        (ROOT / "assets" / f"skin-habit-mark-{lang}.svg").write_text(venn_svg(standalone=True), encoding="utf-8")
    L, PREFIX = "id", ""
    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    print("wrote sitemap.xml, robots.txt")

if __name__ == "__main__":
    main()
