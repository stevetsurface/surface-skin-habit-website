"""Patient-facing skin anatomy, recovery, and supplied photography."""
CARE=json.loads((ROOT/'content/recovery-guides.json').read_text())
def care_field(p,k):return p.get(k if EN else k+'_id',p.get(k,''))
def care_profile(t=None,d=None):
 if d:
  key={'hydraderm':'facial','aquapure-h2o':'facial','oxy-gun':'facial','diamond-peel':'microderm','chemical-peel':'peel','biaxis-qs-laser':'light','ipl-cellec':'light','hifu-liftera':'hifu','pollogen-rf':'rf','nanopore':'needle','pdt-celluma':'led'}.get(d['slug'],'facial')
 else:
  name=t.get('name','').lower();dev=t.get('device')
  if dev:return care_profile(d=next((x for x in C['education']['devices'] if x['slug']==dev),{'slug':dev}))
  key='botox' if 'botulinum' in name else ('acneshot' if 'acne shots' in name else ('inject' if t.get('family')=='inject' else 'facial'))
 return CARE[key]

def recovery_section(t=None,d=None):
 p=care_profile(t,d)
 common=care_field(p,'common');risk=care_field(p,'risks');down=care_field(p,'downtime')
 emergency=tr('Contact the clinic if discomfort is increasing, redness is spreading, blisters appear, or recovery is different from what was explained. Seek urgent medical care for vision changes, breathing or swallowing difficulty, or severe symptoms.','Hubungi klinik jika nyeri meningkat, kemerahan meluas, muncul lepuh, atau pemulihan berbeda dari penjelasan. Segera cari pertolongan medis bila ada gangguan penglihatan, bernapas atau menelan, atau gejala berat.')
 b=title(tr('A LITTLE PREPARATION HELPS','SEDIKIT PERSIAPAN MEMBANTU'),tr('Recovery, without the guesswork.','Pahami pemulihanmu.'),tr('Most expected reactions are temporary. Knowing what is usual—and what needs a call—helps you plan with confidence.','Sebagian besar reaksi yang diharapkan bersifat sementara. Kenali yang umum serta kapan perlu menghubungi klinik agar lebih siap.'))
 b+='<div class="recovery-summary"><article><span class="kicker">'+tr('TIME TO PLAN','WAKTU UNTUK DIRENCANAKAN')+'</span><h3>'+tr('Downtime','Waktu pemulihan')+'</h3><p>'+down+'</p></article><article><span class="kicker">'+tr('OFTEN TEMPORARY','BIASANYA SEMENTARA')+'</span><h3>'+tr('What you may notice','Yang mungkin terasa')+'</h3><p>'+common+'</p></article></div>'
 b+='<div class="recovery-details"><details><summary>'+tr('Potential risks and side effects','Potensi risiko dan efek samping')+'</summary><p>'+risk+'</p></details><details><summary>'+tr('Before your treatment','Sebelum treatment')+'</summary><p>'+care_field(p,'prepare')+'</p></details><details><summary>'+tr('When to contact us','Kapan perlu menghubungi kami')+'</summary><p>'+emergency+'</p>'+link(tr('Contact the clinic ↗','Hubungi klinik ↗'),'https://wa.me/6281222346115')+'</details></div><p class="disclaimer">'+tr('Your clinician explains the exact protocol and your personal risk factors before treatment. A combination may have a different recovery period from any one step.','Klinisi menjelaskan protokol serta faktor risiko pribadimu sebelum treatment. Pemulihan kombinasi dapat berbeda dari satu langkahnya saja.')+'</p>'+link(tr('Clinical safety reference ↗','Referensi keselamatan klinis ↗'),p['source'])
 if care_field(p,'source_note'):b+='<p class="disclaimer">'+care_field(p,'source_note')+'</p>'
 return section(b,'recovery-section','recovery')

def layer_url():return tr('skin-layers.html','lapisan-kulit.html')
LAYER_CONTENT=[
 ('surface','01','Epidermis','Epidermis','Surface & pigment','Permukaan & pigmen','Your outer barrier. Surface texture and some pigment concerns involve this area. Pigment can also lie deeper, so a dark spot is not a diagnosis.','Lapisan pelindung luar. Tekstur permukaan dan sebagian masalah pigmen melibatkan area ini. Pigmen juga bisa lebih dalam; flek gelap bukan diagnosis.','Gentle cleansing, selected superficial peels, and doctor-selected pigment treatments work in different ways.','Pembersihan lembut, peeling superfisial tertentu, dan treatment pigmen pilihan dokter bekerja dengan cara berbeda.','TONE'),
 ('dermis','02','Dermis','Dermis','Collagen & texture','Kolagen & tekstur','A supportive layer containing collagen, elastin, vessels, and skin structures. Fine lines and scars are more complex than surface roughness.','Lapisan penopang berisi kolagen, elastin, pembuluh, dan struktur kulit. Garis halus serta bekas luka lebih kompleks daripada kulit kasar di permukaan.','Microneedling and RF can trigger different renewal responses; they are not interchangeable and do not use the same depth.','Microneedling dan RF dapat memicu respons pembaruan berbeda; keduanya tidak saling menggantikan dan kedalamannya tidak sama.','TEXTURE'),
 ('fat','03','Subcutaneous tissue','Jaringan subkutan','Volume & cushioning','Volume & bantalan','Fat and connective tissue beneath the dermis help shape and cushion an area. Less volume is not automatically a better outcome.','Lemak dan jaringan ikat di bawah dermis membantu membentuk serta melindungi area. Volume lebih sedikit tidak otomatis lebih baik.','Contouring needs an assessment of anatomy and the actual device or injectable product—not just a treatment name.','Kontur perlu penilaian anatomi serta alat atau produk injeksi yang sebenarnya—bukan sekadar nama treatment.','TIGHTEN'),
 ('support','04','Deeper connective support','Penopang jaringan ikat lebih dalam','Support & lifting','Penopang & lifting','Deeper connective structures, including the facial SMAS, are beneath the skin. Anatomy varies by area; this is not a separate universal skin layer.','Struktur ikat lebih dalam, termasuk SMAS wajah, berada di bawah kulit. Anatomi berbeda menurut area; ini bukan lapisan kulit universal tersendiri.','Focused ultrasound uses selected focal depths. Your doctor chooses the device, area, and settings; the illustration does not prescribe a depth.','Ultrasound terfokus memakai kedalaman fokus terpilih. Dokter menentukan alat, area, serta pengaturan; ilustrasi ini tidak menentukan kedalaman tindakan.','TIGHTEN'),
 ('muscle','05','Facial muscle','Otot wajah','Expression & movement','Ekspresi & gerakan','Expression muscles sit beneath and interact with the skin and connective tissues. They are distinct from the dermis.','Otot ekspresi berada di bawah dan berinteraksi dengan kulit serta jaringan ikat. Otot berbeda dari dermis.','Botulinum toxin reduces activity in selected muscles to soften expression lines. It does not exfoliate or tighten a skin layer.','Botulinum toxin mengurangi aktivitas otot tertentu untuk melembutkan garis ekspresi. Ini tidak mengeksfoliasi atau mengencangkan lapisan kulit.','ENHANCE')]

def skin_layers_section(code=None):
 active={'TONE':'surface','CLEAR':'surface','CALM':'surface','TEXTURE':'dermis','TIGHTEN':'support','ENHANCE':'muscle'}.get(code,'surface')
 tabs=''.join('<button class="layer-choice" type="button" data-layer-choice="'+key+'" aria-pressed="'+str(key==active).lower()+'">'+num+' · '+tr(en,id)+'</button>' for key,num,en,id,hen,hid,pen,pid,men,mid,concern in LAYER_CONTENT)
 bands=''.join('<div class="anatomy-band anatomy-'+key+(' selected' if key==active else '')+'" data-anatomy-layer="'+key+'"><span>'+num+'</span><div><b>'+tr(en,id)+'</b><small>'+tr(hen,hid)+'</small></div></div>' for key,num,en,id,hen,hid,*rest in LAYER_CONTENT)
 notes=''.join('<article class="layer-note" data-layer-note="'+key+'" '+('' if key==active else 'hidden')+'><span class="kicker">'+tr(hen,hid)+'</span><h3>'+tr(en,id)+'</h3><p>'+tr(pen,pid)+'</p><p>'+tr(men,mid)+'</p>'+link(tr('Explore related care ↗','Jelajahi perawatan terkait ↗'),slug(concern))+'</article>' for key,num,en,id,hen,hid,pen,pid,men,mid,concern in LAYER_CONTENT)
 return section(title(tr('UNDERSTAND THE LAYERS','PAHAMI LAPISANNYA'),tr('Different targets.<br>Different treatments.','Sasaran berbeda.<br>Perawatan berbeda.'),tr('Deeper does not mean better. The right action depends on your concern, anatomy, and skin—not a ranking of treatment strength.','Lebih dalam bukan berarti lebih baik. Tindakan sesuai kebutuhan, anatomi, dan kulitmu—bukan peringkat kekuatan treatment.'))+'<div class="layer-choices" aria-label="'+tr('Explore skin and underlying structures','Jelajahi kulit dan struktur di bawahnya')+'">'+tabs+'</div><div class="layer-explorer"><div class="anatomy-stack" role="img" aria-label="'+tr('Illustration of skin and deeper tissues, not to scale','Ilustrasi kulit dan jaringan lebih dalam, tidak berskala')+'">'+bands+'<span class="anatomy-caption">'+tr('Schematic only · skin thickness and anatomy vary by location','Skema saja · ketebalan dan anatomi berbeda menurut lokasi')+'</span></div><div class="layer-notes" aria-live="polite">'+notes+'</div></div><p class="disclaimer">'+tr('The first three bands illustrate epidermis, dermis, and subcutaneous tissue. The final two show related deeper structures. Light, heat, and needles do not act within perfectly separate boxes.','Tiga bidang pertama menggambarkan epidermis, dermis, serta jaringan subkutan. Dua terakhir adalah struktur terkait di bawahnya. Cahaya, panas, dan jarum tidak bekerja dalam kotak yang terpisah sempurna.')+'</p>'+link(tr('Skin anatomy reference ↗','Referensi anatomi kulit ↗'),'https://www.hse.gov.uk/skin/professional/structure.htm'),'layers-section','skin-layers')

def layers_page():return hero(tr('HOW YOUR SKIN WORKS','CARA KULITMU BEKERJA'),tr('Know the layer.<br>Understand the care.','Kenali lapisannya.<br>Pahami perawatannya.'),tr('An interactive guide to the skin and the tissues underneath—built to make the consultation easier to follow.','Panduan interaktif kulit serta jaringan di bawahnya agar konsultasi lebih mudah dipahami.'))+skin_layers_section().replace('id="skin-layers"','id="content"')+care_journey()

PHOTO_MAP={'hydraderm':'hydraderm','aquapure-h2o':'hydraderm','oxy-gun':'hydraderm','chemical-peel':'lhala-peel','biaxis-qs-laser':'qs-laser','ipl-cellec':'ipl','hifu-liftera':'hifu','pollogen-rf':'rf-face','nanopore':'nanopore'}
# Existing source-labelled photos are mapped only to the matching procedure.
PHOTO_MAP.pop('aquapure-h2o');PHOTO_MAP.pop('oxy-gun');PHOTO_MAP.pop('nanopore')
def treatment_photo(t=None,d=None):
 if t and 'Botulinum' in t['name']:return 'assets/treatments/botox.jpg'
 if t and t['name']=='LHALA Peel':return 'assets/treatments/lhala-peel.jpg'
 key=PHOTO_MAP.get(d['slug'] if d else t.get('device'))
 return 'assets/treatments/'+key+'.jpg' if key else None

# Supplied result comparisons keep their source privacy masks; no false clinical approval claim.
def results_section(code=None,device=None,treatment=None,limit=None):
 items=[]
 for x in C.get('results',{}).get('items',[]):
  if not(x.get('publish') and x.get('publication_basis') and (OUT/x.get('comparison','missing')).is_file()):continue
  if code and x.get('concern')!=code:continue
  if device and device not in x.get('devices',[]):continue
  if treatment and treatment not in x.get('treatments',[]):continue
  items.append(x)
 if limit:items=items[:limit]
 if not items:return ''
 cards=''.join('<article class="result-card"><div class="comparison-image">'+img(x['comparison'],x['treatment']+' — '+tr('before and after','sebelum dan sesudah'))+'</div><div class="result-info"><span class="kicker">'+e(field(x,'timeframe'))+'</span><h3>'+e(x['treatment'])+'</h3><p>'+e(field(x,'caption'))+'</p></div></article>' for x in items)
 return section(title(tr('SURFACE TREATMENT EXAMPLES','CONTOH TREATMENT SURFACE'),tr('Before & after.<br>With the context that matters.','Sebelum & sesudah.<br>Dengan konteks yang penting.'),tr('Real examples from the Surface menu supplied for this website. Session counts are stated; elapsed time was not provided.','Contoh nyata dari menu Surface yang diberikan untuk situs ini. Jumlah sesi dicantumkan; waktu antar foto tidak diberikan.'))+'<div class="result-grid">'+cards+'</div><p class="disclaimer">'+tr('Individual results vary. These comparisons may differ in lighting, angle, expression, and timing; they are not a controlled study or a guarantee. Source privacy masking has been preserved.','Hasil individu berbeda. Perbandingan dapat berbeda dalam cahaya, sudut, ekspresi, dan waktu; bukan studi terkontrol atau jaminan hasil. Masking privasi sumber dipertahankan.')+'</p>'+link(tr('See all supplied examples ↗','Lihat semua contoh yang diberikan ↗'),results_url()),id='results')

_prev_device=device_page
_prev_treatment=treatment_page
# Build the original treatment content with relevant results, not every case in the library.
def device_page(d):
 body=_base_device_page(d)+explainer_for(d)+recovery_section(d=d)+results_section(device=d['slug'])+care_journey()
 photo=treatment_photo(d=d)
 if photo:body=body.replace('<section class="page-hero ">','<section class="page-hero with-photo">',1).replace('</section>','<div class="page-visual">'+img(photo,d['name'],loading='eager')+'</div></section>',1)
 return body

def treatment_page(t):
 # The existing renderer uses results_section() globally; temporarily suppress that insertion.
 global results_section
 real=results_section;results_section=lambda *a,**kw:''
 try:body=_prev_treatment(t)
 finally:results_section=real
 d=next((x for x in C['education']['devices'] if x['slug']==t.get('device')),None)
 addition=recovery_section(t=t)+real(device=d['slug'] if d else None,treatment=None if d else t['name'])
 marker='<section class="section journey-section"'
 body=body.replace(marker,addition+marker,1)
 photo=treatment_photo(t,d)
 if photo:body=body.replace('<section class="page-hero ">','<section class="page-hero with-photo">',1).replace('</section>','<div class="page-visual">'+img(photo,t['name'],loading='eager')+'</div></section>',1)
 return body

_prev_programme=programme
def programme(code):
 body=_prev_programme(code)
 marker='<section class="section faq-section"'
 extra=skin_layers_section(code)
 body=body.replace(marker,extra+marker,1)
 photo={'CLEAR':'hydraderm','TONE':'qs-laser','TEXTURE':'nanopore','TIGHTEN':'rf-face','ENHANCE':'botox'}.get(code)
 if photo:
  body=re.sub(r'(<div class="page-visual"><img src=")[^"]+',lambda m:m[1]+asset('assets/treatments/'+photo+'.jpg'),body,count=1)
 return body

_prev_education=education_page
def education_page():return _prev_education()+section(title(tr('START WITH THE SKIN','MULAI DARI KULIT'),tr('What happens below the surface?','Apa yang terjadi di bawah permukaan?'))+link(tr('Explore the interactive skin layers ↗','Jelajahi lapisan kulit interaktif ↗'),layer_url(),'button'))
_prev_home=home
def home():return _prev_home()+section(title(tr('UNDERSTAND YOUR CARE','PAHAMI PERAWATANMU'),tr('A concern is only the beginning.','Keluhan adalah titik awal.'))+link(tr('See how treatments act on skin ↗','Lihat cara treatment bekerja pada kulit ↗'),layer_url(),'button'))
_prev_footer=footer
def footer():return _prev_footer().replace('<b>'+tr('Explore','Jelajahi')+'</b>','<b>'+tr('Explore','Jelajahi')+'</b>'+link(tr('How skin layers work','Cara kerja lapisan kulit'),layer_url(),'')+link(tr('Before & after examples','Contoh sebelum & sesudah'),results_url(),''))
_prev_extra_routes=extra_routes
def extra_routes():
 global EN
 _prev_extra_routes()
 for language in ['id','en']:
  EN=language=='en';render(OUT/('en' if EN else '')/layer_url(),layers_page(),tr('Skin layers & treatment targets','Lapisan kulit & sasaran treatment'),'../lapisan-kulit.html' if EN else 'en/skin-layers.html')

_prev_results_page=results_page
def results_page():return _prev_results_page().replace('href="#content"','href="#results"')
