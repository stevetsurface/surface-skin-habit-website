"""Shared visual refinement and an editorial clinic homepage."""
_design_home=home
def home():
 body=_design_home()
 intro='<section class="surface-intro"><div class="intro-copy"><span class="kicker">'+tr('SURFACE SKIN HABIT · SINCE 2014','SURFACE SKIN HABIT · SEJAK 2014')+'</span><h1>'+tr('Good skin.<br>At your<br><em>own pace.</em>','Kulit terawat.<br>Dengan<br><em>ritmemu.</em>')+'</h1><p>'+tr('A little clarity. A personal plan. Doctor-led care that fits your skin and your life.','Sedikit kejelasan. Rencana personal. Perawatan bersama dokter, sesuai kulit dan hidupmu.')+'</p><div class="intro-actions">'+link(tr('Find my skin pathway ↗','Temukan jalur kulitku ↗'),'#concern','button')+link(tr('Meet your doctor','Kenali doktermu'),'dokter.html')+'</div><div class="intro-proof"><span>2014<small>'+tr('Our story began','Awal cerita kami')+'</small></span><span>4<small>'+tr('Jakarta-area clinics','Klinik area Jakarta')+'</small></span><span>'+tr('You','Kamu')+'<small>'+tr('At the centre of care','Pusat perawatan kami')+'</small></span></div></div><div class="intro-gallery"><div class="intro-main">'+img('assets/clinics/tsm-koridor-2.jpg',tr('Welcome to Surface TSM Cibubur','Selamat datang di Surface TSM Cibubur'),loading='eager')+'<div class="intro-caption"><span>'+tr('A SPACE TO FEEL AT EASE','RUANG UNTUK MERASA NYAMAN')+'</span><b>'+tr('Come as you are.','Datang apa adanya.')+'</b></div></div><div class="intro-detail">'+img('assets/clinics/tsm-resepsi.jpg',tr('A quiet corner inside Surface','Sudut tenang di Surface'))+'</div><span class="intro-stamp">SKIN CARE.<br>SELF CARE.<br>SURFACE.</span></div></section>'
 body=re.sub(r'<section class="page-hero with-photo">.*?</section>',lambda m:intro,body,count=1,flags=re.S)
 return body

# Appllama research: Skin Bliss routine starter menu (1385561364/oth_sjz4a).
# Adapt choice cards and progressive disclosure; keep Surface's own content and assets.
def starting_point():
 choices='';previews=''
 for row in FLOW_DATA:
  code,en,id,*_=row
  choices+='<button type="button" class="start-choice" data-start-choice="'+code+'" aria-pressed="false" aria-controls="start-'+code+'"><span>'+code+'</span><b>'+tr(en,id)+'</b><i aria-hidden="true">↗</i></button>'
  previews+='<article data-start-preview="'+code+'" id="start-'+code+'" hidden><span class="kicker">'+tr('YOUR STARTING POINT','TITIK AWALMU')+'</span><h3>'+tr(en,id)+'</h3><p>'+tr('Start with a doctor assessment. Explore the options and recovery before deciding on a procedure.','Mulai dari penilaian dokter. Pahami pilihan serta pemulihan sebelum memutuskan tindakan.')+'</p><div class="start-next"><a href="'+flow_url()+'?concern='+code+'#treatment-flow"><span>01</span><div><b>'+tr('See my visual pathway','Lihat alur visualku')+'</b><small>'+tr('Understand the decisions and review points','Pahami keputusan serta tahap tinjauan')+'</small></div><i>↗</i></a><a href="'+slug(code)+'"><span>02</span><div><b>'+tr('Explore care options','Jelajahi pilihan perawatan')+'</b><small>'+tr('Treatments, prices, and what to expect','Treatment, harga, serta yang perlu diketahui')+'</small></div><i>↗</i></a></div>'+link(tr('Discuss this with a doctor ↗','Bahas bersama dokter ↗'),'menu.html?concern='+code+'#book','button')+'</article>'
 return '<dialog id="starting-point" aria-labelledby="starting-title"><div class="start-top"><span class="kicker">SURFACE · '+tr('A LITTLE CLARITY','SEDIKIT KEJELASAN')+'</span><button type="button" data-close-start aria-label="'+tr('Close guide','Tutup panduan')+'">×</button></div><h2 id="starting-title">'+tr('What brings you here?','Apa yang ingin kamu rawat?')+'</h2><p>'+tr('Choose what is on your mind. You do not need to know the treatment name.','Pilih yang ingin kamu bahas. Tidak perlu tahu nama treatment-nya.')+'</p><div class="start-choices">'+choices+'</div><div class="start-previews" aria-live="polite">'+previews+'</div><p class="start-note">'+tr('A guide to explore care, not a diagnosis. Your doctor confirms suitability.','Panduan menjelajahi perawatan, bukan diagnosis. Dokter memastikan kesesuaiannya.')+'</p></dialog>'
_picker_home=home
def home():
 body=_picker_home();needle=link(tr('Find my skin pathway ↗','Temukan jalur kulitku ↗'),'#concern','button')
 return body.replace(needle,'<button type="button" class="button" data-open-start>'+tr('Find my starting point ↗','Temukan titik awalku ↗')+'</button>',1)
_picker_menu=menu_page
def menu_page():
 return _picker_menu().replace('</section>','<button type="button" class="button menu-start" data-open-start>'+tr('Help me choose a starting point ↗','Bantu pilih titik awalku ↗')+'</button></section>',1)
_picker_footer=footer
def footer():return _picker_footer()+starting_point()
