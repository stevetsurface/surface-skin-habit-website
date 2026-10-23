"""Described photo placeholders and more photography (Steve, 23 Oct 2026).

Every slot states what the photo should be, in both languages, so the shot list lives on the pages
themselves. Slots never use the draft-copy wording that check.py rejects."""

def photo_slot(en,id,ratio='4/3',cls=''):
 text=tr(en,id)
 return f'<div class="photo-slot {cls}" style="aspect-ratio:{ratio}" role="img" aria-label="{e(text)}"><span class="kicker">{tr("PHOTO TO COME","FOTO MENYUSUL")}</span><p>{e(text)}</p></div>'

PATHWAY_TILE={
 'CLEAR':('Close-up of a cheek with mild active acne and blackheads: bare skin, soft daylight, no makeup, no filter.','Close-up pipi dengan jerawat ringan dan komedo: kulit polos, cahaya siang lembut, tanpa makeup, tanpa filter.'),
 'TONE':('Cheek and temple with sun spots and uneven tone in daylight, no retouching. Skin colour is never promised, so no result pair here.','Pipi dan pelipis dengan flek dan warna tidak rata di cahaya siang, tanpa retouch. Warna kulit tidak dijanjikan, jadi tanpa pasangan foto hasil.'),
 'TEXTURE':('Skin texture close-up: enlarged pores and shallow acne scars, side light to show relief.','Close-up tekstur kulit: pori besar dan bekas jerawat dangkal, cahaya samping agar relief terlihat.'),
 'CALM':('Reactive skin with mild redness on the cheeks, calm expression, soft even light.','Kulit reaktif dengan kemerahan ringan di pipi, ekspresi tenang, cahaya lembut merata.'),
 'TIGHTEN':('Jawline and neck in three-quarter profile, natural light, no filter.','Garis rahang dan leher dari sudut tiga perempat, cahaya alami, tanpa filter.'),
 'ENHANCE':('Relaxed natural face at rest, front view, even light, to talk about proportion and symmetry.','Wajah rileks tampak depan, cahaya merata, untuk bicara proporsi dan simetri.'),
}
IN_PROGRESS={
 'CLEAR':('Hydraderm handpiece on the cheek, therapist hands in gloves, device visible.','Handpiece Hydraderm di pipi, tangan terapis bersarung, alat terlihat.'),
 'TONE':('The doctor applying the LHALA Peel with a brush, timer in frame.','Dokter mengaplikasikan LHALA Peel dengan kuas, timer terlihat.'),
 'TEXTURE':('Nanopore or Dermapen in the doctor’s hand over the cheek, focus on the device.','Nanopore atau Dermapen di tangan dokter di atas pipi, fokus pada alat.'),
 'CALM':('Red PDT light over the face, customer relaxed, room dimmed.','Cahaya merah PDT di atas wajah, pelanggan rileks, ruangan redup.'),
 'TIGHTEN':('HIFU or RF handpiece along the jawline, device screen visible.','Handpiece HIFU atau RF di sepanjang garis rahang, layar alat terlihat.'),
 'ENHANCE':('The doctor marking the face before an injection, no needle in frame.','Dokter menandai wajah sebelum injeksi, tanpa jarum dalam bingkai.'),
}
PAIR_EN='Before / week 12 pair: same angle, same light, no filter, written consent and doctor sign-off. 800×1000 each.'
PAIR_ID='Pasangan Awal / Minggu ke-12: sudut dan cahaya sama, tanpa filter, izin tertulis dan tanda tangan dokter. 800×1000 per foto.'

def pair_slot():
 return '<div class="pair-slot">'+photo_slot(tr('Before','Awal')+'. '+PAIR_EN,'Awal. '+PAIR_ID,'4/5')+photo_slot(tr('Week 12','Minggu ke-12')+'. '+PAIR_EN,'Minggu ke-12. '+PAIR_ID,'4/5')+'</div>'

def pair_slots_section(code=None,n=2):
 pairs=''.join(pair_slot() for _ in range(n))
 note=tr('No result photos for the Tone pathway: we do not advertise changes in skin colour with photos.','Tidak ada foto hasil untuk jalur Tone: perubahan warna kulit tidak kami iklankan dengan foto.') if code=='TONE' else tr('Published only with written consent, at week 12 or later, signed off by the responsible doctor.','Dipublikasikan hanya dengan izin tertulis, minimal minggu ke-12, ditandatangani dokter penanggung jawab.')
 if code=='TONE':return section(title(tr('RESULT PHOTOS','FOTO HASIL'),tr('Why there are none here.','Mengapa tidak ada di sini.'))+'<p class="pair-note">'+note+'</p>')
 return section(title(tr('MORE RESULTS TO COME','HASIL BERIKUTNYA'),tr('Week 0 to week 12.<br>Same light, same angle.','Minggu 0 ke minggu 12.<br>Cahaya dan sudut sama.'))+'<div class="pair-slots">'+pairs+'</div><p class="pair-note">'+note+'</p>')

def pathway_photo_strip():
 tiles=''
 for i,o in enumerate(C['concerns']):
  en,id=PATHWAY_TILE[o['code']]
  tiles+='<a href="'+slug(o['code'])+'">'+photo_slot(en,id,'4/5')+'<h3>0'+str(i+1)+' · '+e(o['name'])+'</h3><p class="small">'+e(field(o,'title'))+'</p></a>'
 return section(title(tr('SIX PATHWAYS, SIX KINDS OF SKIN','ENAM JALUR, ENAM JENIS KULIT'),tr('Real skin.<br>In daylight.','Kulit asli.<br>Di cahaya siang.'),tr('Photographed at Surface, with consent, no filters.','Difoto di Surface, dengan izin, tanpa filter.'))+'<div class="pathway-photos">'+tiles+'</div>')

_slots_home=home
def home():
 body=_slots_home()
 m=re.search(r'<section class="section care-index-section".*?</section>',body,flags=re.S)
 extra=pathway_photo_strip()+results_section(limit=3)+section('<div class="section-link">'+link(tr('All documented results ↗','Semua hasil terdokumentasi ↗'),results_url())+'</div>')
 return body[:m.end()]+extra+body[m.end():] if m else body+extra

_slots_doctor_cards=doctor_cards
def doctor_cards(full=False):
 return _slots_doctor_cards(full).replace('<span class="doctor-monogram" aria-hidden="true">S</span>',photo_slot('Doctor portrait: half body, Surface uniform, plain light background, soft daylight. 1000×1200.','Potret dokter: setengah badan, seragam Surface, latar polos terang, cahaya lembut. 1000×1200.','4/5'))

_slots_clinics_page=clinics_page
def clinics_page():
 body=_slots_clinics_page()
 return re.sub(r'<div class="clinic-letter">([^<]+)</div>',lambda m:'<div class="clinic-image">'+photo_slot('Surface '+m[1]+': entrance and reception in daytime, then one treatment room. 1200×800 each.','Surface '+m[1]+': pintu masuk dan resepsi di siang hari, lalu satu ruang treatment. 1200×800 per foto.','3/2')+'</div>',body)

_slots_programme=programme
def programme(code):
 body=_slots_programme(code)
 pairs=pair_slots_section(code)
 m=re.search(r'<section class="section [^"]*"[^>]*>(?:(?!</section>).)*?result-grid.*?</section>',body,flags=re.S)
 if m:body=body[:m.end()]+pairs+body[m.end():]
 else:body=body.replace('<section class="section faq-section"',pairs+'<section class="section faq-section"',1)
 en,id=IN_PROGRESS[code]
 prog=section('<div class="progress-photo">'+photo_slot(en,id,'3/2')+'<div>'+label('IN THE TREATMENT ROOM','DI RUANG TREATMENT')+'<h2>'+tr('What a session looks like.','Seperti apa satu sesi.')+'</h2><p>'+tr('Hands, device and skin. The doctor or therapist who does it, in the room where it happens.','Tangan, alat dan kulit. Dokter atau terapis yang mengerjakannya, di ruang tempat itu terjadi.')+'</p></div></div>')
 return body.replace('<section class="section journey-section"',prog+'<section class="section journey-section"',1)

def _hero_slot(body,en,id):
 if 'page-hero with-photo' in body:return body
 return body.replace('<section class="page-hero ">','<section class="page-hero with-photo">',1).replace('</section>','<div class="page-visual">'+photo_slot(en,id,'4/3')+'</div></section>',1)

_slots_device_page=device_page
def device_page(d):
 return _hero_slot(_slots_device_page(d),d['name']+' in a Surface treatment room: three-quarter angle, screen on, no people. 1200×900.',d['name']+' di ruang treatment Surface: sudut tiga perempat, layar menyala, tanpa orang. 1200×900.')

_slots_treatment_page=treatment_page
def treatment_page(t):
 return _hero_slot(_slots_treatment_page(t),t['name']+' in progress: hands and device or product on skin, clean room, face out of frame unless consented. 1200×900.',t['name']+' sedang berjalan: tangan dan alat atau produk di kulit, ruang bersih, wajah di luar bingkai kecuali ada izin. 1200×900.')

_slots_results_page=results_page
def results_page():
 body=_slots_results_page()
 blocks=''.join('<h3 class="pair-heading">'+e(o['name'])+' · '+e(field(o,'title'))+'</h3>'+(pair_slots_section(o['code'],2) if o['code']!='TONE' else pair_slots_section('TONE')) for o in C['concerns'])
 return body+section(title(tr('WHAT WE ARE COLLECTING NEXT','YANG SEDANG KAMI KUMPULKAN'),tr('Week 0 and week 12,<br>for every pathway.','Minggu 0 dan minggu 12,<br>untuk setiap jalur.'),tr('The pairs above came from earlier Surface material and state session counts, not elapsed time. New pairs follow one rule: same angle, same light, twelve weeks apart, with consent.','Pasangan di atas berasal dari materi Surface sebelumnya dan menyebut jumlah sesi, bukan jarak waktu. Pasangan baru mengikuti satu aturan: sudut sama, cahaya sama, berjarak dua belas minggu, dengan izin.'))+blocks)
