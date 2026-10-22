"""Shared brand, education, story, and consultation journey features."""
def safe_slug(text):return re.sub(r'[^a-z0-9]+','-',text.lower()).strip('-')
def treatment_url(t):return 'treatment-'+safe_slug(t['name'])+'.html'
def story_url():return tr('our-story.html','cerita-kami.html')
def visit_url():return tr('your-visit.html','kunjunganmu.html')
def stories_url():return tr('customer-stories.html','cerita-pelanggan.html')
def results_url():return tr('results.html','hasil.html')
def brand_section():
 names=['Biaxis Q-Switched Nd:YAG','Cellec V IPL','Pollogen TriPollar RF','Mediderma Nanopore','Celluma PDT','Dermalogica','Dermapen 4','Juvelook']
 items=[]
 for name in names:
  b=next(x for x in C['education']['brands'] if x['name']==name);logo=b.get('logo','')
  visual=img('assets/brands/'+logo,name) if (OUT/'assets/brands'/logo).is_file() else '<b>'+e(name)+'</b>'
  items.append('<a class="brand-tile" href="edukasi-brand.html">'+visual+'<span>'+e(name)+'</span></a>')
 return section(title(tr('KNOW WHAT’S IN YOUR CARE','KENALI PERAWATANMU'),tr('The names behind your treatment.','Nama di balik treatment-mu.'),tr('Explore selected devices and product brands in the Surface catalogue. Your doctor explains what is used in your plan.','Kenali pilihan alat dan merek dalam katalog Surface. Dokter menjelaskan yang digunakan dalam rencanamu.'))+'<div class="brand-wall">'+''.join(items)+'</div><div class="section-link">'+link(tr('Explore all devices & brands ↗','Jelajahi semua alat & merek ↗'),'edukasi-brand.html')+'</div>',id='brands')
def story_excerpt():
 return section('<div>'+label('SURFACE, SINCE 2014','SURFACE, SEJAK 2014')+'<h2>'+tr('Many people.<br>One personal approach.','Banyak orang.<br>Satu pendekatan personal.')+'</h2><p>'+tr('Since 2014, Surface has cared for people with different skin concerns. Today, that care continues across four Jakarta-area clinics—one conversation, one personal plan, one skin habit at a time.','Sejak 2014, Surface merawat banyak orang dengan beragam kebutuhan kulit. Kini, perawatan berlanjut di empat klinik area Jakarta—satu percakapan, satu rencana personal, satu kebiasaan kulit pada satu waktu.')+'</p>'+link(tr('Read our story ↗','Baca cerita kami ↗'),story_url())+'</div><div class="story-numbers"><div><b>2014</b><span>'+tr('Our story began','Cerita kami dimulai')+'</span></div><div><b>4</b><span>'+tr('Connected clinics','Klinik terhubung')+'</span></div><div><b>1</b><span>'+tr('Plan that starts with you','Rencana yang dimulai darimu')+'</span></div></div>','story-excerpt','our-story')
def story_page():
 return hero(tr('OUR STORY · SINCE 2014','CERITA KAMI · SEJAK 2014'),tr('Care that grows<br>with you.','Perawatan yang tumbuh<br>bersamamu.'),tr('Many people, many skin journeys. A personal approach that remains at the heart of Surface.','Banyak orang, banyak perjalanan kulit. Pendekatan personal tetap menjadi inti Surface.'),'assets/clinics/tsm-koridor.jpg')+section('<div class="article-body single-article"><h2>'+tr('A skin habit, built over time.','Kebiasaan kulit, dibangun seiring waktu.')+'</h2><p>'+tr('Surface began in 2014. Over the years, we have cared for people seeking help with acne, pigmentation, texture, sensitivity, and changes in skin quality. Everyone arrives with a different story.','Surface dimulai pada 2014. Selama perjalanan ini, kami merawat banyak orang yang membutuhkan bantuan untuk jerawat, pigmentasi, tekstur, sensitivitas, dan perubahan kualitas kulit. Setiap orang datang dengan cerita berbeda.')+'</p><p>'+tr('Our approach starts with the concern. Understand what is happening, choose care with a doctor, and review progress together. A course of care gives each visit a purpose beyond the appointment itself.','Pendekatan kami dimulai dari kebutuhan kulit. Pahami kondisinya, pilih perawatan bersama dokter, lalu tinjau perkembangannya. Rencana perawatan membuat setiap kunjungan punya tujuan yang berkelanjutan.')+'</p><p>'+tr('Today, you can find Surface at Setiabudi, CITOS, Lippo Mall Puri, and TSM Cibubur. Your care stays personal as your needs evolve.','Kini, Surface hadir di Setiabudi, CITOS, Lippo Mall Puri, dan TSM Cibubur. Perawatan tetap personal saat kebutuhanmu berubah.')+'</p></div>',id='content')+approach()+brand_section()+section(link(tr('Meet our Surface Friends ↗','Kenali Sahabat Surface ↗'),stories_url(),'button'))
def customer_stories():
 cards=''
 for item in C.get('published_stories',[]):
  cards+='<article class="story-card"><span class="story-mark" aria-hidden="true">↗</span><p>'+e(field(item,'summary'))+'</p><h3>'+e(item['name'])+'</h3><span class="story-treatment">'+e(item['treatment'])+'</span>'+link(tr('Read the original story ↗','Baca cerita asli ↗'),item['source'])+'</article>'
 reviews=''.join(link(c['short']+' ↗',c['google_reviews'],'review-clinic') for c in C['clinics'])
 return section(title(tr('SURFACE FRIENDS','SAHABAT SURFACE'),tr('Experiences, in their own way.','Pengalaman dari sudut pandang mereka.'),tr('Summaries of stories previously published on Surface’s website. Individual experiences are not a promise of results.','Ringkasan cerita yang sudah dipublikasikan di situs Surface. Pengalaman individu bukan janji hasil.'))+'<div class="story-cards">'+cards+'</div><div class="review-links"><span>'+tr('More clinic reviews on Google','Ulasan klinik lainnya di Google')+'</span>'+reviews+'</div>',id='customer-stories')
def story_listing():return hero(tr('CUSTOMER STORIES','CERITA PELANGGAN'),tr('Real experiences.<br>Personal journeys.','Pengalaman nyata.<br>Perjalanan personal.'),tr('Read attributed stories from Surface’s published archive and independent clinic reviews.','Baca cerita dari arsip Surface dan ulasan klinik independen.'))+customer_stories().replace('id="customer-stories"','id="content"')

def care_journey():
 stages=[('01','Understand','Pahami','Choose a concern. Read what the treatment does and what to expect.','Pilih keluhan. Pahami cara kerja treatment dan yang bisa diharapkan.'),('02','Book a conversation','Booking konsultasi','Choose a clinic and a preferred time. Our team confirms availability on WhatsApp.','Pilih klinik dan waktu pilihan. Tim mengonfirmasi ketersediaan melalui WhatsApp.'),('03','Agree on your plan','Sepakati rencanamu','Ask about suitability, recovery, cost, and the next review before deciding.','Tanyakan kesesuaian, pemulihan, biaya, dan tinjauan berikutnya sebelum memutuskan.'),('04','Review & return','Tinjau & kembali','Follow your clinician’s aftercare and agree when to review your skin.','Ikuti instruksi pascaperawatan dari klinisi dan sepakati kapan kulit ditinjau kembali.')]
 return section(title(tr('FROM FIRST MESSAGE TO FOLLOW-UP','DARI PESAN PERTAMA HINGGA TINDAK LANJUT'),tr('Every visit has a next step.','Setiap kunjungan punya langkah berikutnya.'))+'<div class="care-stages">'+''.join('<article><span>'+n+'</span><h3>'+tr(a,b)+'</h3><p>'+tr(c,d)+'</p></article>' for n,a,b,c,d in stages)+'</div><div class="section-link">'+link(tr('Plan your first or next visit ↗','Rencanakan kunjungan pertama atau berikutnya ↗'),visit_url())+'</div>','journey-section')
def visit_page():
 blocks=[('Before you arrive','Sebelum datang','Share your main concern and preferred clinic. Bring your skincare list and tell the doctor about recent treatments, medicines, allergies, and relevant medical history during consultation.','Sampaikan keluhan utama dan klinik pilihan. Bawa daftar skincare dan ceritakan treatment terakhir, obat, alergi, serta riwayat medis yang relevan saat konsultasi.'),('During your consultation','Saat konsultasi','Ask what the treatment targets, why it is recommended, what alternatives exist, and what recovery could look like. Ask for the full price before agreeing.','Tanyakan sasaran treatment, alasan rekomendasi, alternatif, dan perkiraan pemulihan. Minta harga lengkap sebelum menyetujui.'),('Before you leave','Sebelum pulang','Ask for written aftercare, a contact for concerns, the next review date, and how your doctor will assess progress. A follow-up is a care decision, not an automatic purchase.','Minta instruksi pascaperawatan tertulis, kontak bila ada keluhan, tanggal tinjauan berikutnya, dan cara dokter menilai perkembangan. Tindak lanjut adalah keputusan perawatan, bukan pembelian otomatis.'),('Between visits','Di antara kunjungan','Follow your clinician’s instructions. Contact the clinic if recovery differs from what was explained. For severe or urgent symptoms, seek urgent medical care.','Ikuti instruksi klinisi. Hubungi klinik bila pemulihan berbeda dari penjelasan. Untuk gejala berat atau mendesak, segera cari pertolongan medis.')]
 return hero(tr('YOUR SURFACE VISIT','KUNJUNGAN SURFACE-MU'),tr('Arrive informed.<br>Leave with a plan.','Datang dengan pemahaman.<br>Pulang dengan rencana.'),tr('A practical guide to your first consultation and your follow-up visits.','Panduan praktis konsultasi pertama dan kunjungan tindak lanjut.'))+section('<div class="visit-guide">'+''.join('<article><span class="kicker">0'+str(i+1)+'</span><h2>'+tr(a,b)+'</h2><p>'+tr(c,d)+'</p></article>' for i,(a,b,c,d) in enumerate(blocks))+'</div><div class="return-cta"><h3>'+tr('Already visited Surface?','Sudah pernah ke Surface?')+'</h3><p>'+tr('Request a doctor review or your next appointment.','Minta tinjauan dokter atau janji temu berikutnya.')+'</p>'+link(tr('Request a follow-up ↗','Minta tindak lanjut ↗'),'#book','button followup-link')+'</div>',id='content')+care_journey()

DEVICE_MODE={
 'biaxis-qs-laser':('pigment','Pigment-focused light','Cahaya untuk pigmen','Short laser pulses are absorbed by selected pigment. Your doctor chooses the wavelength and settings for the type of spot.','Pulsa laser singkat diserap pigmen tertentu. Dokter memilih panjang gelombang dan pengaturan sesuai jenis flek.','https://www.asds.net/skin-experts/skin-conditions/hyperpigmentation'),
 'ipl-cellec':('light','Filtered light, selected targets','Cahaya tersaring, sasaran terpilih','IPL uses filtered broad-spectrum light rather than a single laser wavelength. Pigment and fine vessels absorb light energy and convert it to heat.','IPL memakai cahaya spektrum luas tersaring, bukan satu panjang gelombang laser. Pigmen dan pembuluh halus menyerap energi cahaya dan mengubahnya menjadi panas.','https://www.isaps.org/discover/patients-home/procedures/non-surgical-procedures/laser-skin-rejuvenation/'),
 'chemical-peel':('surface','Controlled surface renewal','Pembaruan permukaan terukur','A peel applies a selected chemical solution to exfoliate skin. The ingredient and strength determine its action and recovery.','Peeling menggunakan larutan kimia terpilih untuk mengeksfoliasi kulit. Bahan dan kekuatannya menentukan cara kerja dan pemulihan.','https://www.aad.org/public/cosmetic/younger-looking/chemical-peels-overview'),
 'nanopore':('needle','A controlled renewal response','Respons pembaruan terukur','Fine needles create controlled punctures that stimulate a healing response and collagen production. Depth and treatment settings matter.','Jarum halus membuat tusukan terukur yang merangsang respons pemulihan dan produksi kolagen. Kedalaman dan pengaturan treatment penting.','https://www.aad.org/public/cosmetic/scars-stretch-marks/microneedling-fade-scars'),
 'pollogen-rf':('dermis','Heat within the dermis','Panas di dalam dermis','Radiofrequency delivers heat within skin to stimulate collagen remodelling. This is different from surface exfoliation.','Radiofrekuensi memberikan panas di dalam kulit untuk merangsang pembentukan ulang kolagen. Ini berbeda dari eksfoliasi permukaan.','https://pollogen.com/technologies/tripollar/'),
 'pdt-celluma':('light','Light, without abrasion','Cahaya tanpa pengikisan','LED treatment uses selected wavelengths. Blue light targets acne-associated bacteria; red light is used for different skin responses. It does not scrub or peel the skin.','LED memakai panjang gelombang terpilih. Cahaya biru menargetkan bakteri terkait jerawat; cahaya merah digunakan untuk respons kulit berbeda. Ini tidak menggosok atau mengelupas kulit.','https://www.celluma.com/pages/faq')}

def skin_diagram(mode,heading,copy,source=None):
 diagram='<div class="skin-cutaway '+mode+'" role="img" aria-label="'+tr('Simplified skin layers; illustration, not a treatment-depth measurement','Lapisan kulit sederhana; ilustrasi, bukan pengukuran kedalaman treatment')+'"><span class="energy-mark" aria-hidden="true">↓ ↓ ↓</span><div class="layer epidermis"><span>'+tr('Epidermis','Epidermis')+'</span></div><div class="layer dermis"><span>'+tr('Dermis · collagen support','Dermis · penopang kolagen')+'</span><i></i><i></i><i></i></div><div class="layer support"><span>'+tr('Underlying tissue','Jaringan di bawahnya')+'</span></div></div>'
 return section('<div>'+label('WHAT HAPPENS IN YOUR SKIN','YANG TERJADI DI KULITMU')+'<h2>'+heading+'</h2><p>'+copy+'</p><p class="disclaimer">'+tr('A simplified illustration. Treatment depth, suitability, and response vary by device and settings.','Ilustrasi sederhana. Kedalaman, kesesuaian, dan respons treatment berbeda menurut alat dan pengaturan.')+'</p>'+ (link(tr('Read the clinical explanation ↗','Baca penjelasan klinis ↗'),source) if source else '')+'</div>'+diagram,'skin-explainer')

def explainer_for(d):
 data=DEVICE_MODE.get(d['slug'])
 if data:
  mode,en,id,body_en,body_id,source=data
  return skin_diagram(mode,tr(en,id),tr(body_en,body_id),source)
 return skin_diagram('surface',tr('Understand the action, not just the name.','Pahami cara kerjanya, bukan hanya namanya.'),e(field(d,'how')))

_base_device_page=device_page
def device_page(d):return _base_device_page(d)+explainer_for(d)+results_section()+care_journey()

def treatment_page(t):
 d=next((d for d in C['education']['devices'] if d['slug']==t.get('device')),None)
 family=next((f for f in C['education']['treatment_families'] if f['code']==t['family']),{})
 facts=[(tr('Appointment','Kunjungan'),str(t['duration_min'])+tr(' minutes',' menit') if t.get('duration_min') else tr('Discuss at consultation','Bahas saat konsultasi')),(tr('Performed by','Dilakukan oleh'),tr('Doctor','Dokter') if t.get('performed_by')=='doctor' else tr('Therapist','Terapis')),(tr('Single session','Sesi satuan'),rp(t.get('price'))),(tr('Interval','Interval'),field(t,'interval',tr('Set by your doctor','Ditentukan dokter')))]
 b=hero(tr('TREATMENT EXPLAINER','PENJELASAN TREATMENT'),e(t['name']),e(field(t,'for')))
 b+=section('<div class="device-facts">'+''.join('<div><span>'+a+'</span><p>'+e(str(v))+'</p></div>' for a,v in facts)+'</div><div class="article-body single-article"><h2>'+tr('What this treatment is for','Tujuan treatment ini')+'</h2><p>'+e(field(t,'for'))+'</p><h2>'+tr('How it works','Cara kerjanya')+'</h2><p>'+e(field(d,'how') if d else field(t,'mechanism',field(family,'blurb')))+'</p><p>'+e(field(t,'note'))+'</p>'+ (link(tr('Read more about the mechanism ↗','Baca cara kerjanya lebih lanjut ↗'),t['mechanism_source']) if t.get('mechanism_source') else '')+'<h2>'+tr('The device or products','Alat atau produk')+'</h2><p>'+e(t.get('brand','Surface'))+'</p>'+ (link(tr('Explore the device guide ↗','Jelajahi panduan alat ↗'),'edukasi-'+d['slug']+'.html') if d else link(tr('Explore devices & brands ↗','Jelajahi alat & merek ↗'),'edukasi-brand.html'))+'<h2>'+tr('What to expect afterwards','Yang diharapkan setelahnya')+'</h2><p>'+e(field(d,'downtime') if d else tr('Recovery depends on the procedure and your skin. Ask the doctor about expected effects and the plan for follow-up.','Pemulihan bergantung pada tindakan dan kulitmu. Tanyakan efek yang diharapkan serta rencana tindak lanjut kepada dokter.'))+'</p><p class="disclaimer">'+tr('This guide explains the listed treatment. Your doctor confirms the appropriate protocol, price, and recovery for your skin.','Panduan ini menjelaskan treatment dalam katalog. Dokter memastikan protokol, harga, dan pemulihan yang sesuai untuk kulitmu.')+'</p></div>',id='content')
 if d:b+=explainer_for(d)
 return b+results_section()+care_journey()

def treatment_directory():
 body=hero(tr('TREATMENT LIBRARY','PUSTAKA TREATMENT'),tr('Know your treatment.<br>Understand your skin.','Kenali treatment-mu.<br>Pahami kulitmu.'),tr('Plain-language guides to each treatment in the Surface catalogue: purpose, mechanism, products, appointment, and recovery.','Panduan sederhana setiap treatment dalam katalog Surface: tujuan, cara kerja, produk, kunjungan, dan pemulihan.'))
 for f in C['education']['treatment_families']:
  ts=[t for t in C['education']['treatments'] if t['family']==f['code']]
  if not ts:continue
  body+=section(title(tr('EXPLORE','JELAJAHI'),e(field(f,'name')),e(field(f,'blurb')))+'<div class="resource-grid">'+''.join('<a class="resource-card" href="'+treatment_url(t)+'"><span class="kicker">'+e(t.get('brand','Surface'))+'</span><h3>'+e(t['name'])+'</h3><p>'+e(field(t,'for'))+'</p><span class="text-link">'+tr('How it works ↗','Cara kerjanya ↗')+'</span></a>' for t in ts)+'</div>',id='content' if 'id="content"' not in body else '')
 return body

def relevant_treatments(code):
 devices={'CLEAR':['hydraderm','chemical-peel','pdt-celluma'],'TONE':['biaxis-qs-laser','ipl-cellec','chemical-peel'],'TEXTURE':['nanopore','diamond-peel'],'CALM':['aquapure-h2o','pdt-celluma','oxy-gun'],'TIGHTEN':['pollogen-rf','hifu-liftera'],'ENHANCE':[]}[code]
 cards=''
 for ds in devices:
  d=next((d for d in C['education']['devices'] if d['slug']==ds),None)
  if not d:continue
  cards+='<a class="resource-card" href="edukasi-'+d['slug']+'.html"><span class="kicker">'+tr('HOW IT WORKS','CARA KERJANYA')+'</span><h3>'+e(d['name'])+'</h3><p>'+e(field(d,'how'))+'</p><span class="text-link">'+tr('See the skin explainer ↗','Lihat penjelasan kulit ↗')+'</span></a>'
 if not cards:
  ts=[t for t in C['education']['treatments'] if t['family']=='inject']
  cards=''.join('<a class="resource-card" href="'+treatment_url(t)+'"><span class="kicker">'+tr('DOCTOR-LED','BERSAMA DOKTER')+'</span><h3>'+e(t['name'])+'</h3><p>'+e(field(t,'for'))+'</p><span class="text-link">'+tr('Understand your options ↗','Pahami pilihanmu ↗')+'</span></a>' for t in ts[:3])
 return section(title(tr('BEHIND YOUR PLAN','DI BALIK RENCANAMU'),tr('What does it actually do?','Apa yang sebenarnya dilakukan?'))+'<div class="resource-grid">'+cards+'</div><div class="section-link">'+link(tr('Explore every treatment ↗','Jelajahi semua treatment ↗'),'edukasi-treatment.html')+'</div>')

def results_section(code=None):
 items=[]
 for x in C.get('results',{}).get('items',[]):
  if x.get('publish') and x.get('consent') and x.get('doctor_approved') and (not code or x.get('concern')==code):
   if all((OUT/x.get(k,'missing')).is_file() for k in ['before','after']):items.append(x)
 if not items:return ''
 cards=''.join('<article class="result-card"><div class="result-pair"><figure>'+img(x['before'],tr('Before treatment','Sebelum treatment'))+'<figcaption>'+tr('Before','Sebelum')+'</figcaption></figure><figure>'+img(x['after'],tr('After treatment','Setelah treatment'))+'<figcaption>'+tr('After','Setelah')+'</figcaption></figure></div><h3>'+e(x['treatment'])+'</h3><p>'+e(field(x,'caption'))+'</p><span>'+e(x['timeframe'])+'</span></article>' for x in items)
 return section(title(tr('DOCUMENTED PROGRESS','PERKEMBANGAN TERDOKUMENTASI'),tr('Before & after. With context.','Sebelum & sesudah. Dengan konteks.'))+'<div class="result-grid">'+cards+'</div><p class="disclaimer">'+tr('Individual results vary. Images are published with consent and treatment context.','Hasil individu berbeda. Foto dipublikasikan dengan persetujuan dan konteks treatment.')+'</p>',id='results')
def results_page():
 return hero(tr('PATIENT RESULTS','HASIL PASIEN'),tr('Progress needs context.','Perkembangan perlu konteks.'),tr('Treatment, timing, and comparable photographs matter more than a dramatic image.','Treatment, waktu, dan foto yang sebanding lebih penting daripada gambar dramatis.'))+(results_section() or section('<div class="article-body single-article"><h2>'+tr('Talk through real examples at consultation.','Bahas contoh nyata saat konsultasi.')+'</h2><p>'+tr('No before-and-after photo pairs are published here yet. Ask your doctor about comparable examples, the treatment used, number of visits, timeframe, and the range of possible outcomes.','Belum ada pasangan foto sebelum-sesudah yang dipublikasikan di sini. Tanyakan kepada dokter tentang contoh sebanding, treatment, jumlah kunjungan, waktu, dan rentang hasil yang mungkin.')+'</p>'+link(tr('Ask about your concern ↗','Tanyakan kebutuhanmu ↗'),'#book','button')+'</div>',id='content'))

_base_home=home
def home():return _base_home()+story_excerpt()+brand_section()+customer_stories()+care_journey()
_base_programme=programme
def programme(code):
 body=_base_programme(code)
 insert=relevant_treatments(code)+results_section(code)+care_journey()
 return body.replace('<section class="section faq-section"',insert+'<section class="section faq-section"',1)
_base_header=header
def header(twin):
 s=_base_header(twin)
 return s.replace('</nav>',link(tr('Our story','Cerita kami'),story_url(),'')+'</nav>')
_base_footer=footer
def footer():
 s=_base_footer()
 return s.replace('<b>'+tr('Meet Surface','Kenali Surface')+'</b>','<b>'+tr('Meet Surface','Kenali Surface')+'</b>'+link(tr('Our story','Cerita kami'),story_url(),'')+link(tr('Customer stories','Cerita pelanggan'),stories_url(),'')+link(tr('Plan your visit','Rencanakan kunjungan'),visit_url(),''))
_base_booking=booking
def booking(interest=''):
 s=_base_booking(interest)
 extra='<label for="visit-type">'+tr('YOUR VISIT','KUNJUNGANMU')+'</label><select id="visit-type"><option value="first">'+tr('First consultation','Konsultasi pertama')+'</option><option value="followup">'+tr('Doctor review / follow-up','Tinjauan dokter / tindak lanjut')+'</option><option value="return">'+tr('Returning for my next treatment','Kembali untuk treatment berikutnya')+'</option></select><div class="booking-time"><div><label for="preferred-date">'+tr('PREFERRED DATE (OPTIONAL)','TANGGAL PILIHAN (OPSIONAL)')+'</label><input type="date" id="preferred-date"></div><div><label for="preferred-time">'+tr('PREFERRED TIME','WAKTU PILIHAN')+'</label><select id="preferred-time"><option value="flexible">'+tr('Flexible','Fleksibel')+'</option><option value="morning">'+tr('Morning','Pagi')+'</option><option value="afternoon">'+tr('Afternoon','Siang / sore')+'</option><option value="evening">'+tr('Evening','Malam')+'</option></select></div></div>'
 s=s.replace('<button class="button" type="submit">',extra+'<button class="button" type="submit">')
 return s

def extra_routes():
 global EN
 for lang in ['id','en']:
  EN=lang=='en';base=OUT/('en' if EN else '')
  specs=[(story_url(),'our-story.html','cerita-kami.html',story_page,tr('Our story · Since 2014','Cerita kami · Sejak 2014')),(visit_url(),'your-visit.html','kunjunganmu.html',visit_page,tr('Your visit & follow-up','Kunjungan & tindak lanjut')),(stories_url(),'customer-stories.html','cerita-pelanggan.html',story_listing,tr('Customer stories','Cerita pelanggan')),(results_url(),'results.html','hasil.html',results_page,tr('Treatment results','Hasil treatment'))]
  for route,en,id,fn,titletext in specs:render(base/route,fn(),titletext,('../'+id) if EN else ('en/'+en))
  for t in C['education']['treatments']:
   route=treatment_url(t);render(base/route,treatment_page(t),t['name'],('../'+route) if EN else ('en/'+route))
