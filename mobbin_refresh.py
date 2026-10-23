"""Mobbin-informed editorial browsing and explicit consultation request summary."""
def concerns():
 rows='';panels=''
 for n,row in enumerate(FLOW_DATA):
  code,en,id,h1,i1,p1,q1,h2,i2,p2,q2,h3,i3,p3,q3,devices,source=row
  rows+='<button type="button" data-care-choice="'+code+'" aria-pressed="'+str(n==0).lower()+'" aria-controls="care-'+code+'"><span>0'+str(n+1)+'</span><b>'+code.capitalize()+'</b><small>'+tr(en,id)+'</small><i aria-hidden="true">↗</i></button>'
  panels+='<article data-care-panel="'+code+'" id="care-'+code+'" '+('' if n==0 else 'hidden')+'><span class="kicker">'+tr('YOUR SKIN, UNDERSTOOD','PAHAMI KULITMU')+'</span><h3>'+tr(en,id)+'</h3><p>'+tr(p1,q1)+'</p><ol><li>'+tr(h1,i1)+'</li><li>'+tr(h2,i2)+'</li><li>'+tr(h3,i3)+'</li></ol><div class="care-panel-links">'+link(tr('Explore this care pathway ↗','Jelajahi jalur perawatan ↗'),slug(code),'button')+link(tr('View the visual map','Lihat peta visual'),flow_url()+'?concern='+code+'#treatment-flow')+'</div><span class="care-footnote">'+tr('Your doctor confirms the plan, recovery, and price before treatment.','Dokter memastikan rencana, pemulihan, dan harga sebelum treatment.')+'</span></article>'
 return section(title(tr('THE CARE INDEX','INDEKS PERAWATAN'),tr('Start with your skin.<br>We’ll take it from here.','Mulai dari kulitmu.<br>Kita cari langkahnya bersama.'),tr('Six concerns. Different possibilities. Select one to see where your conversation could begin.','Enam kebutuhan. Beragam kemungkinan. Pilih satu untuk melihat titik awal percakapanmu.'))+'<div class="care-index"><div class="care-index-list" aria-label="'+tr('Skin concerns','Keluhan kulit')+'">'+rows+'</div><div class="care-index-panels" aria-live="polite">'+panels+'</div></div>','care-index-section','concern')

_mobbin_home=home
def home():
 body=_mobbin_home()
 hero='<section class="editorial-hero">'+img('assets/clinics/tsm-koridor-2.jpg',tr('A member of the Surface team at TSM Cibubur','Tim Surface di TSM Cibubur'),loading='eager')+'<div class="editorial-hero-copy"><span class="kicker">'+tr('SURFACE SKIN HABIT · SINCE 2014','SURFACE SKIN HABIT · SEJAK 2014')+'</span><h1>'+tr('A little care.<br>A lasting<br><em>skin habit.</em>','Sedikit perawatan.<br>Kebiasaan baik<br><em>untuk kulitmu.</em>')+'</h1><p>'+tr('Understand your skin. Find your pace.<br>Build a personal plan with a doctor.','Pahami kulitmu. Temukan ritmemu.<br>Susun rencana personal bersama dokter.')+'</p><div class="editorial-actions"><button type="button" class="button" data-open-start>'+tr('Find my starting point ↗','Temukan titik awalku ↗')+'</button>'+link(tr('Explore our care ↓','Jelajahi perawatan ↓'),'#concern')+'</div></div><div class="editorial-location"><span>'+tr('YOUR NEIGHBOURHOOD SURFACE','SURFACE DI DEKATMU')+'</span><b>Setiabudi · CITOS · Lippo Mall Puri · TSM Cibubur</b></div></section>'
 return re.sub(r'<section class="surface-intro">.*?</section>',lambda m:hero,body,count=1,flags=re.S)

_mobbin_booking=booking
def booking(interest=''):
 body=_mobbin_booking(interest)
 summary='<aside class="request-summary" aria-label="'+tr('Your consultation request','Permintaan konsultasimu')+'"><span class="kicker">'+tr('YOUR CONSULTATION REQUEST','PERMINTAAN KONSULTASIMU')+'</span><h3>'+tr('A clear next step.','Langkah berikutnya jelas.')+'</h3><dl><div><dt>'+tr('Clinic','Klinik')+'</dt><dd data-request-value="clinic"></dd></div><div><dt>'+tr('Concern','Keluhan')+'</dt><dd data-request-value="interest"></dd></div><div><dt>'+tr('Visit','Kunjungan')+'</dt><dd data-request-value="visit-type"></dd></div><div><dt>'+tr('Preferred date','Tanggal pilihan')+'</dt><dd data-request-value="preferred-date"></dd></div><div><dt>'+tr('Preferred time','Waktu pilihan')+'</dt><dd data-request-value="preferred-time"></dd></div></dl><p>'+tr('These are your preferences. Our team confirms availability and your appointment on WhatsApp.','Ini adalah preferensimu. Tim kami memastikan ketersediaan serta jadwal melalui WhatsApp.')+'</p></aside>'
 return body.replace('<form ',summary+'<form ',1)

# Real Surface photography makes care and the clinic tangible.
def photo_treatments():
 cards=[]
 for photo,name,url,en,id in [
  ('hydraderm','Hydraderm Facial','treatment-hydraderm-facial.html','See what happens during a facial.','Lihat proses perawatan facial.'),
  ('qs-laser','QS Laser','edukasi-biaxis-qs-laser.html','Understand the light, the skin, and recovery.','Pahami cahaya, kulit, dan pemulihannya.'),
  ('hifu','HIFU','edukasi-hifu-liftera.html','Explore how ultrasound is used in care.','Kenali penggunaan ultrasound dalam perawatan.')]:
  cards.append('<a class="photo-treatment" href="'+url+'">'+img('assets/treatments/'+photo+'.jpg',name+' — Surface Skin Habit')+'<div><span class="kicker">'+tr('TREATMENT, EXPLAINED','KENALI TREATMENT')+'</span><h3>'+name+' <span aria-hidden="true">↗</span></h3><p>'+tr(en,id)+'</p><span class="photo-detail-link">'+tr('How it works · Downtime · Risks','Cara kerja · Downtime · Risiko')+'</span></div></a>')
 return section(title(tr('A CLOSER LOOK','LIHAT LEBIH DEKAT'),tr('Care you can picture.','Bayangkan perawatanmu.'),tr('A look inside selected Surface treatments. Open a guide to understand the process and what to expect afterwards.','Lihat beberapa treatment Surface. Buka panduannya untuk memahami proses dan apa yang diharapkan setelahnya.'))+'<div class="photo-treatment-grid">'+''.join(cards)+'</div>','photo-treatment-section','care-in-focus')

_photo_home=home
def home():
 body=_photo_home()
 return body.replace('<section class="section care-index-section"',photo_treatments()+'<section class="section care-index-section"',1)

_photo_story_excerpt=story_excerpt
def story_excerpt():
 body=_photo_story_excerpt()
 return body.replace('<div class="story-numbers">','<div class="story-photo-column">'+img('assets/clinics/dinding-good-skin.jpg',tr('A prepared treatment bed beneath the Good Skin Is In sign at Surface','Tempat perawatan di bawah tulisan Good Skin Is In di Surface'))+'<div class="story-numbers">',1).replace('</section>','</div></section>',1)

def clinic_photo_journal():
 return section(title(tr('INSIDE SURFACE','DI DALAM SURFACE'),tr('Get to know the space.','Kenali ruang perawatanmu.'))+'<div class="clinic-photo-journal"><figure>'+img('assets/clinics/tsm-resepsi.jpg',tr('Surface reception at TSM Cibubur','Resepsionis Surface TSM Cibubur'))+'<figcaption>'+tr('A welcome at Surface TSM Cibubur.','Selamat datang di Surface TSM Cibubur.')+'</figcaption></figure><figure>'+img('assets/clinics/ruang-treatment-1.jpg',tr('Prepared treatment beds inside Surface','Tempat perawatan di Surface'))+'<figcaption>'+tr('A look inside the treatment space.','Suasana ruang perawatan.')+'</figcaption></figure></div>','clinic-photo-section')

_photo_story_page=story_page
def story_page():
 return _photo_story_page()+clinic_photo_journal()

_photo_visit_page=visit_page
def visit_page():
 body=_photo_visit_page()
 return body.replace('</section>','</section>'+clinic_photo_journal(),1)

_photo_menu_page=menu_page
def menu_page():
 body=_photo_menu_page()
 return body.replace('</section>','</section>'+photo_treatments(),1)
