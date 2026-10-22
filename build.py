"""Build all Surface routes from the bilingual catalogue and retained specialist content."""
from pathlib import Path
from html import escape as e, unescape
from html.parser import HTMLParser
from urllib.parse import quote
import json,re,shutil,hashlib
ROOT=Path(__file__).resolve().parent
OUT=ROOT; CONTENT=ROOT/'content'; C=json.loads((CONTENT/'catalog.json').read_text())
ORIGIN='https://stevetsurface.github.io/surface-skin-habit-website'
EN=True

def tr(en,id):return en if EN else id
def field(obj,key,default=''):return obj.get(key+'_en',obj.get(key,default)) if EN else obj.get(key,default)
def rp(n):return tr('Price at consultation','Harga saat konsultasi') if n is None else (tr('Free','Gratis') if n==0 else 'Rp '+f'{n:,}'.replace(',','.'))
def asset(p):return ('../' if EN else '')+p
def slug(code):return field(C['streams'][code],'slug')+'.html'
def link(text,url,cls='text-link'):return f'<a class="{cls}" href="{e(url)}">{text}</a>'
def img(src,alt,cls='',loading='lazy'):return f'<img src="{asset(src)}" alt="{e(alt)}" class="{cls}" loading="{loading}">'
def label(en,id):return f'<span class="kicker">{tr(en,id)}</span>'
def section(body,cls='',id=''):return f'<section class="section {cls}"'+(f' id="{id}"' if id else '')+f'>{body}</section>'
def title(k,h,p=''):return f'<div class="section-title"><div><span class="kicker">{k}</span><h2>{h}</h2></div>'+ (f'<p>{p}</p>' if p else '')+'</div>'
def brand():return '<a class="brand" href="index.html" aria-label="Surface Skin Habit">'+img('assets/logo-mark.png','',loading='eager')+'<span class="wordmark">SURFACE<small>SKIN HABIT</small></span></a>'
def header(twin):
 return f'''<a class="skip" href="#main">{tr('Skip to content','Langsung ke konten')}</a><header class="header">{brand()}<nav id="navigation" aria-label="{tr('Main navigation','Navigasi utama')}">{link(tr('Skin concerns','Keluhan kulit'),'index.html#concern','')}{link(tr('Treatments & prices','Treatment & harga'),'menu.html','')}{link(tr('Our doctors','Dokter kami'),'dokter.html','')}{link(tr('Clinics','Klinik'),'klinik.html','')}{link(tr('Journal','Jurnal'),'blog.html','')}</nav><div class="header-right"><a class="language" href="{twin}" lang="{'id' if EN else 'en'}" aria-label="{tr('Bahasa Indonesia','English')}">{tr('ID','EN')}</a>{link(tr('Book a consultation','Booking konsultasi')+' ↗','#book','button small desktop')}<button class="menu" aria-expanded="false" aria-controls="navigation" aria-label="{tr('Open menu','Buka menu')}">☰</button></div></header>'''
def footer():
 return '<footer><div class="footer-top">'+brand()+f'<p>{tr("A little care. A lasting habit.","Perawatan kecil. Kebiasaan bermakna.")}</p></div><div class="footer-grid"><div><p>{tr("Doctor-led skin care at four Jakarta-area clinics.","Perawatan kulit bersama dokter di empat klinik area Jakarta.")}</p>{link("Instagram ↗","https://www.instagram.com/surfaceskinhabit/","")}</div><div><b>{tr("Explore","Jelajahi")}</b>'+''.join(link(tr(a,b),c,'') for a,b,c in [('Skin concerns','Keluhan kulit','index.html#concern'),('Treatments & prices','Treatment & harga','menu.html'),('Skin education','Edukasi kulit','edukasi.html'),('Journal','Jurnal','blog.html')])+f'</div><div><b>{tr("Meet Surface","Kenali Surface")}</b>'+''.join(link(tr(a,b),c,'') for a,b,c in [('Our doctors','Dokter kami','dokter.html'),('Our clinics','Klinik kami','klinik.html'),('Our approach','Pendekatan kami','metode.html')])+f'</div><div><b>{tr("Let’s talk","Hubungi kami")}</b>{link("0812 2234 6115 ↗","https://wa.me/6281222346115","")}<span>{tr("Daily","Setiap hari")} · 09.00–22.00 WIB</span></div></div><div class="legal">© 2026 Surface Skin Habit<span>{tr("Results vary. Suitability is assessed by a doctor.","Hasil dapat berbeda. Kesesuaian treatment dinilai dokter.")}</span></div></footer><a class="mobile-book" href="#book">{tr("Book a free consultation","Booking konsultasi gratis")} <span>↗</span></a><script src="{asset("assets/redesign.js")}" defer></script>'
def booking(interest=''):
 options=''.join(f'<option value="{o["name"]}">{o["short"]}</option>' for o in C['clinics'])
 interests=''.join(f'<option value="{o["name"]}" '+('selected' if interest==o['code'] else '')+f'>{o["name"]} — {e(field(o,"title"))}</option>' for o in C['concerns'])
 return section(f'''<div>{label('YOUR NEXT CHAPTER','LANGKAH BERIKUTNYA')}<h2>{tr('Good skin starts<br>with a conversation.','Kulit terawat dimulai<br>dari percakapan.')}</h2><p>{tr('Tell us what’s on your mind. Start with a free doctor consultation at your nearest Surface clinic.','Ceritakan kebutuhan kulitmu. Mulai dengan konsultasi dokter gratis di klinik Surface terdekat.')}</p><span class="availability">● {tr('WhatsApp replies daily','WhatsApp dibalas setiap hari')}, 09.00–22.00 WIB</span></div><form id="booking-form" data-language="{tr('en','id')}"><label for="clinic">{tr('YOUR PREFERRED CLINIC','PILIH KLINIK')}</label><select id="clinic" required><option value="">{tr('Choose a clinic','Pilih klinik')}</option>{options}</select><label for="interest">{tr('I’D LIKE TO DISCUSS','SAYA INGIN MEMBAHAS')}</label><select id="interest"><option value="general">{tr('My skin concerns','Kebutuhan kulit saya')}</option>{interests}</select><button class="button" type="submit">{tr('Continue on WhatsApp','Lanjut ke WhatsApp')} <span>↗</span></button><p class="form-note">{tr('Choose a clinic, then message our team to request a time. Your appointment is confirmed in chat.','Pilih klinik, lalu hubungi tim kami untuk jadwal. Janji temu dikonfirmasi melalui chat.')}</p></form>''','booking','book')
def hero(k,h,p,photo=None):
 b=f'<div class="hero-copy"><span class="kicker">{k}</span><h1>{h}</h1><p>{p}</p><div class="actions">{link(tr("Book a free consultation","Booking konsultasi gratis")+" ↗","#book","button")}{link(tr("Explore below ↓","Jelajahi lebih lanjut ↓"),"#content")}</div></div>'
 if photo:b+='<div class="page-visual">'+img(photo,'Surface Skin Habit',loading='eager')+'</div>'
 return f'<section class="page-hero {"with-photo" if photo else ""}">{b}</section>'
def concerns():
 cards=''.join(f'<a class="concern" href="{slug(o["code"])}"><span class="concern-number">0{i+1} / {o["name"].upper()}</span><h3>{e(field(o,"title"))}</h3><p>{e(field(o,"intro"))}</p><span class="round-arrow" aria-hidden="true">↗</span></a>' for i,o in enumerate(C['concerns']))
 return section(title(tr('LET’S START WITH YOU','MULAI DARI KEBUTUHANMU'),tr('What’s on your skin’s mind?','Apa yang kulitmu butuhkan?'),tr('Six pathways. Your doctor helps you find a personal plan.','Enam jalur. Dokter membantu memilih rencana yang sesuai.'))+f'<div class="concerns">{cards}</div><div class="quiet-link">'+link(tr('Not sure? Try our skin analysis ↗','Belum yakin? Coba analisis kulit ↗'),'analisis.html')+'</div>',id='concern')
def approach():
 steps=[('Understand','Pahami','Meet your doctor and discuss your skin, goals, and history.','Temui dokter dan bahas kulit, tujuan, serta riwayat perawatanmu.'),('Personalise','Sesuaikan','Understand your options and the price before you decide.','Pahami pilihan treatment dan harga sebelum memutuskan.'),('Review & maintain','Tinjau & pelihara','Review progress together and decide what comes next.','Tinjau perkembangan bersama dokter dan tentukan langkah selanjutnya.')]
 return section(title(tr('THE SKIN HABIT APPROACH','PENDEKATAN SKIN HABIT'),tr('A plan for your skin.<br>A pace for your life.','Rencana untuk kulitmu.<br>Ritme untuk hidupmu.'))+'<div class="steps">'+''.join(f'<article><span>0{i+1}</span><h3>{tr(a,b)}</h3><p>{tr(c,d)}</p></article>' for i,(a,b,c,d) in enumerate(steps))+'</div>','journey-section')
def doctor_cards(full=False):
 cards=''
 for d in C['doctors']:
  if not d.get('publish'):continue
  if not full and not d.get('photo'):continue
  names=' · '.join(next(x['short'] for x in C['clinics'] if x['code']==code) for code in d['clinics'])
  photo=img(d['photo'],d['name']) if d.get('photo') else '<span class="doctor-monogram" aria-hidden="true">S</span>'
  detail=('<p>'+e(field(d,'bio'))+'</p><ul>'+''.join('<li>'+e(a)+'</li>' for a in field(d,'creds',[]))+'</ul>'+link('Instagram ↗','https://www.instagram.com/'+d['instagram']+'/')) if full else link(tr('Meet your doctor ↗','Kenali doktermu ↗'),'dokter.html')
  cards+=f'<article class="doctor {"full-doctor" if full else ""}" id="doctor-{d["name"].split()[1].lower()}"><div class="portrait">{photo}</div><div class="doctor-info"><h3>{e(d["name"])}</h3><p>{e(field(d,"role"))}<br>{e(names)}</p>{detail}</div></article>'
 return '<div class="doctors '+('full-team' if full else '')+'">'+cards+'</div>'
def team():return section(title(tr('REAL PEOPLE. THOUGHTFUL CARE.','TIM NYATA. PERAWATAN PERSONAL.'),tr('In experienced hands.','Bersama tangan berpengalaman.'))+doctor_cards())
def faq(items):
 return section(f'<div>{label("A LITTLE MORE CLARITY","PAHAMI LEBIH JELAS")}<h2>{tr("It’s okay to<br>have questions.","Wajar bila kamu<br>punya pertanyaan.")}</h2></div><div class="faqs">'+''.join(f'<details><summary>{e(field(q,"q"))}</summary><p>{e(field(q,"a"))}</p></details>' for q in items)+'</div>','faq-section')
def offer_card(o,code):
 prices=''.join(f'<div><span>{tr(a,b)}</span><b>{rp(o[k])}</b></div>' for a,b,k in [('Single session','Satu sesi','single'),('3-session pack','Paket 3 sesi','pack3'),('6-session pack','Paket 6 sesi','pack6')] if o.get(k) is not None)
 if not prices:prices='<div><span>'+tr('Personalised plan','Rencana personal')+'</span><b>'+tr('Quote at consultation','Harga saat konsultasi')+'</b></div>'
 return f'<article class="treatment" data-search="{e(o["name"].lower())}" id="{o["name"].lower().replace(" ","-")}"><span class="kicker">{e(o["level"]).upper()}</span><h3>{e(o["name"])}</h3><p>{e(field(o,"desc"))}</p><ul>'+''.join('<li>'+e(x)+'</li>' for x in field(o,'includes',[]))+f'</ul><p class="treatment-meta">{o["duration_min"]} {tr("minutes","menit")} · {e(field(o,"interval"))}</p><div class="offer-prices">{prices}</div>'+link(tr('Discuss with a doctor ↗','Diskusikan dengan dokter ↗'),'#book','button')+'</article>'
def programme(code):
 o=next(x for x in C['concerns'] if x['code']==code);s=C['streams'][code]
 headlines={'CLEAR':('A clearer path.<br>For your skin.','Langkah lebih jernih.<br>Untuk kulitmu.'),'TONE':('Find your balance.<br>Let your skin shine.','Warna lebih merata.<br>Kulit lebih bercahaya.'),'TEXTURE':('Your next chapter.<br>A smoother feeling.','Babak baru.<br>Tekstur lebih halus.'),'CALM':('A gentler approach.<br>Room to recover.','Pendekatan lembut.<br>Ruang untuk pulih.'),'TIGHTEN':('Care that supports.<br>Confidence that lasts.','Perawatan yang mendukung.<br>Percaya diri berkelanjutan.'),'ENHANCE':('A little refinement.<br>Still entirely you.','Sedikit penyempurnaan.<br>Tetap dirimu seutuhnya.')}
 photo='assets/doctors/devi.jpg' if code=='ENHANCE' else C['images']['stream_'+code]['src']
 body=hero(tr('THE ','JALUR ')+o['name'].upper()+tr(' PATHWAY',''),tr(*headlines[code]),e(field(o,'intro')),photo)
 body+='<nav class="pathway-tabs" aria-label="'+tr('Skin pathways','Jalur kulit')+'">'+''.join(f'<a href="{slug(x["code"])}" '+('aria-current="page"' if x['code']==code else '')+'>'+x['name']+'</a>' for x in C['concerns'])+'</nav>'
 body+=section(f'<div>{label("IS THIS FOR ME?","APAKAH INI UNTUKKU?")}<h2>{e(field(o,"title"))}</h2><p>{tr("Bring your questions. Your doctor will help you understand your options.","Bawa pertanyaanmu. Dokter membantu memahami pilihan yang sesuai.")}</p></div><div class="concern-lines">'+''.join(f'<p><span>0{i+1}</span>{e(v)}</p>' for i,v in enumerate(field(s,'for_you',[])))+'</div>','suitability','content')
 body+=section(title(tr('YOUR TREATMENT OPTIONS','PILIHAN TREATMENT'),tr('A considered approach.','Pendekatan yang terarah.'),tr('Consultation is free. The doctor confirms suitability and price before treatment.','Konsultasi gratis. Dokter memastikan kesesuaian dan harga sebelum treatment.'))+'<div class="treatments">'+''.join(offer_card(x,code) for x in o['offers'] if not (code=='ENHANCE' and x['level']!='start'))+'</div><p class="disclaimer">'+tr('Packages are paid upfront. Results vary. Intervals are reviewed with your doctor.','Paket dibayar di muka. Hasil berbeda pada setiap orang. Interval ditinjau bersama dokter.')+'</p>',id='options')
 body+=approach()+section(title(tr('WHAT YOU CAN EXPECT','YANG DAPAT KAMU HARAPKAN'),tr('Care, with clear boundaries.','Perawatan dengan penjelasan jelas.'))+'<div class="promises"><article><h3>'+tr('Our commitment','Komitmen kami')+'</h3><ul>'+''.join('<li>'+e(x)+'</li>' for x in field(s,'promise',[]))+'</ul></article><article><h3>'+tr('Before you decide','Sebelum memutuskan')+'</h3><ul>'+''.join('<li>'+e(x)+'</li>' for x in field(s,'not',[]))+'</ul></article></div>')+faq(s['faq'])+team()
 return body

def doctors_page():return hero(tr('THE MEDICAL TEAM','TIM MEDIS'),tr('People first.<br>Always.','Utamakan manusia.<br>Selalu.'),tr('Meet the doctors behind your care. Choose a clinic and start with a conversation.','Kenali dokter di balik perawatanmu. Pilih klinik dan mulai dengan percakapan.'),'assets/doctors/kharisma.jpg')+section(doctor_cards(True),id='content')
def clinics_page():
 body=hero(tr('FIND YOUR SURFACE','TEMUKAN SURFACE-MU'),tr('Closer to you.<br>Connected by care.','Lebih dekat denganmu.<br>Terhubung oleh perawatan.'),tr('Four Jakarta-area clinics. One record that follows your care.','Empat klinik area Jakarta. Satu riwayat untuk perjalanan perawatanmu.'),'assets/clinics/tsm-resepsi.jpg')
 body+='<nav class="pathway-tabs">'+''.join(link(x['short'],'#'+x['code'].lower(),'') for x in C['clinics'])+'</nav>'
 for c in C['clinics']:
  photo='assets/clinics/tsm-resepsi.jpg' if c['code']=='TSM' else ('assets/clinics/lmp-treatment-alat.jpg' if c['code']=='LMP' else None)
  visual='<div class="clinic-image">'+img(photo,c['name'])+'</div>' if photo else '<div class="clinic-letter">'+c['short']+'</div>'
  body+=section(f'<div class="clinic-detail">{visual}<div>{label(field(c,"area").upper(),field(c,"area").upper())}<h2>{e(c["name"])}</h2><p>{e(c["address"])}</p><p class="small muted">{tr("Please confirm opening hours and doctor availability when booking.","Konfirmasi jam buka dan jadwal dokter saat booking.")}</p><div class="actions">{link(tr("Get directions ↗","Petunjuk arah ↗"),c["maps"],"button")}{link(tr("Read Google reviews ↗","Baca ulasan Google ↗"),c["google_reviews"])}</div><button class="clinic-book text-link" data-clinic="{c["name"]}">{tr("Book at this clinic ↗","Booking di klinik ini ↗")}</button></div></div>',id=c['code'].lower())
 return body.replace('href="#content"','href="#sb"')
def menu_page():
 body=hero(tr('TREATMENTS & PRICES','TREATMENT & HARGA'),tr('Clear choices.<br>Thoughtful care.','Pilihan jelas.<br>Perawatan terarah.'),tr('Explore the programmes. Compare single sessions and packages. Start with a free doctor consultation.','Jelajahi program. Bandingkan sesi satuan dan paket. Mulai dengan konsultasi dokter gratis.'))
 body+='<nav class="pathway-tabs">'+''.join(link(o['name'],'#'+o['code'].lower(),'') for o in C['concerns'])+'</nav>'
 body+=section('<label class="search-label" for="treatment-search">'+tr('FIND A TREATMENT','CARI TREATMENT')+'</label><input id="treatment-search" type="search" placeholder="'+tr('Search by programme or treatment name…','Cari nama program atau treatment…')+'"><p id="search-empty" hidden>'+tr('No matching treatments. Try another name.','Treatment tidak ditemukan. Coba nama lain.')+'</p>',id='content')
 for o in C['concerns']:
  body+=section(title(o['name'].upper(),e(field(o,'title')),e(field(o,'intro')))+'<div class="treatments">'+''.join(offer_card(x,o['code']) for x in o['offers'] if not(o['code']=='ENHANCE' and x['level']!='start'))+'</div>','price-group',o['code'].lower())
 body+=extras_menu()
 body+=section(link(tr('See the complete single-session price list ↗','Lihat daftar harga satuan lengkap ↗'),'harga-lengkap.html','button')+'<p class="disclaimer">'+e(field(C['site'],'price_note'))+'</p>')
 return body

def extras_menu():
 cards=''
 for o in C['stacks']['items']:
  cards+='<article class="resource-card"><span class="kicker">'+tr('COMBINATION','KOMBINASI')+'</span><h3>'+e(o['name'])+'</h3><p>'+e(field(o,'for'))+'</p><ul>'+''.join('<li>'+e(v)+'</li>' for v in field(o,'includes',[]))+'</ul><b>'+rp(o.get('price'))+'</b>'+link(tr('Discuss suitability ↗','Diskusikan kesesuaian ↗'),'#book')+'</article>'
 body=section(title(tr('IN ONE VISIT','DALAM SATU KUNJUNGAN'),tr('Considered combinations.','Kombinasi yang terarah.'),e(field(C['stacks'],'before')))+'<div class="resource-grid">'+cards+'</div>',id='stack')
 rows=''
 for o in C['addons']:
  rows+='<tr><th scope="row">'+e(o.get('name',''))+'</th><td>'+e(field(o,'for',field(o,'desc','')))+'</td><td>'+rp(o.get('price',o.get('single')))+'</td></tr>'
 return body+section(title('ADD-ONS',tr('A little extra care.','Sedikit perawatan tambahan.'))+'<div class="tx-wrap"><table><thead><tr><th>'+tr('Treatment','Treatment')+'</th><th>'+tr('Concern','Kebutuhan')+'</th><th>'+tr('Price','Harga')+'</th></tr></thead><tbody>'+rows+'</tbody></table></div>',id='addon')

def education_page():
 cards=''.join(f'<a class="resource-card" href="edukasi-{d["slug"]}.html"><span class="kicker">{e(d["family"].upper())}</span><h3>{e(d["name"])}</h3><p>{e(field(d,"how"))}</p><span class="text-link">{tr("Understand the treatment ↗","Pahami treatment ↗")}</span></a>' for d in C['education']['devices'])
 return hero(tr('SKIN EDUCATION','EDUKASI KULIT'),tr('Understand your care.<br>Ask better questions.','Pahami perawatanmu.<br>Tanyakan lebih jauh.'),tr('A guide to the devices, procedures, and decisions behind your treatment plan.','Panduan alat, tindakan, dan pertimbangan di balik rencana perawatanmu.'))+section('<div class="education-nav">'+''.join(link(tr(a,b),c,'button secondary') for a,b,c in [('All treatments','Semua treatment','edukasi-treatment.html'),('Devices & brands','Alat & merek','edukasi-brand.html'),('Combinations','Kombinasi','edukasi-kombinasi.html'),('Treatment intervals','Interval treatment','edukasi-waktu.html')])+'</div><div class="resource-grid">'+cards+'</div><p class="disclaimer">'+e(field(C['education'],'disclaimer'))+'</p>',id='content')
def device_page(d):
 rows=[(tr('Session','Sesi'),str(d['duration_min'])+tr(' minutes',' menit')),(tr('Interval','Interval'),field(d,'interval')),(tr('What it feels like','Yang dirasakan'),field(d,'sensation')),(tr('Recovery','Pemulihan'),field(d,'downtime'))]
 body=hero(tr('TREATMENT GUIDE','PANDUAN TREATMENT'),e(d['name']),e(field(d,'how')))
 body+=section('<div class="device-facts">'+''.join('<div><span>'+a+'</span><p>'+e(b)+'</p></div>' for a,b in rows)+'</div><div class="reading-layout"><aside>'+label('IN THIS GUIDE','DALAM PANDUAN INI')+''.join(link(tr(a,b),'#'+c,'') for a,b,c in [('How it works','Cara kerja','how'),('What it addresses','Kegunaan','uses'),('Before treatment','Sebelum treatment','before'),('Aftercare','Setelah treatment','aftercare')])+'</aside><div class="article-body"><section id="how"><h2>'+tr('How it works','Cara kerjanya')+'</h2>'+''.join('<p>'+e(p)+'</p>' for p in field(d,'detail').split('\n\n'))+'</section><section id="uses"><h2>'+tr('What it addresses','Kegunaannya')+'</h2><ul>'+''.join('<li>'+e(v)+'</li>' for v in field(d,'treats',[]))+'</ul></section><section id="before"><h2>'+tr('Discuss with your doctor','Diskusikan dengan dokter')+'</h2><ul>'+''.join('<li>'+e(v)+'</li>' for v in field(d,'avoid_if',[]))+'</ul></section><section id="aftercare"><h2>'+tr('Aftercare','Setelah perawatan')+'</h2><ul>'+''.join('<li>'+e(v)+'</li>' for v in field(d,'aftercare',[]))+'</ul></section><p class="disclaimer">'+e(field(C['education'],'disclaimer'))+'</p></div></div>',id='content')
 return body

def blog_page(post=None):
 if post:
  return hero(tr('THE SURFACE JOURNAL','JURNAL SURFACE'),e(field(post,'title')),e(field(post,'summary')))+section('<article class="article-body single-article"><p class="kicker">'+post['date']+'</p>'+''.join('<p>'+e(p)+'</p>' for p in field(post,'body',[]))+link(tr('Explore the related pathway ↗','Jelajahi jalur terkait ↗'),slug(post['cta_stream']))+'</article>',id='content')
 return hero(tr('THE SURFACE JOURNAL','JURNAL SURFACE'),tr('A little knowledge.<br>A better conversation.','Sedikit pengetahuan.<br>Percakapan lebih bermakna.'),tr('Notes on skin, treatments, and making informed choices.','Catatan tentang kulit, treatment, dan pilihan yang lebih dipahami.'))+section('<div class="resource-grid">'+''.join(f'<a class="resource-card" href="blog-{field(p,"slug")}.html"><span class="kicker">{p["date"]}</span><h3>{e(field(p,"title"))}</h3><p>{e(field(p,"summary"))}</p><span class="text-link">{tr("Read the story ↗","Baca artikel ↗")}</span></a>' for p in C['posts'])+'</div>',id='content')

class Node:
 def __init__(self,tag='',attrs=None,parent=None):self.tag=tag;self.attrs=dict(attrs or []);self.children=[];self.parent=parent
 def text(self):return ''.join(x.text() if isinstance(x,Node) else x for x in self.children)
 def walk(self):
  yield self
  for x in self.children:
   if isinstance(x,Node):yield from x.walk()
 def remove(self):
  if self.parent and self in self.parent.children:self.parent.children.remove(self)
 def html(self):
  if not self.tag:return ''.join(x.html() if isinstance(x,Node) else x for x in self.children)
  attrs=''.join(' '+k+('="'+e(str(v),quote=True)+'"' if v is not None else '') for k,v in self.attrs.items())
  return '<'+self.tag+attrs+'>'+('' if self.tag in Parser.void else ''.join(x.html() if isinstance(x,Node) else x for x in self.children)+'</'+self.tag+'>')
class Parser(HTMLParser):
 void={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
 def __init__(self,s):super().__init__(convert_charrefs=False);self.root=Node();self.cur=self.root;self.feed(s)
 def handle_starttag(self,t,a):
  n=Node(t,a,self.cur);self.cur.children.append(n)
  if t not in self.void:self.cur=n
 def handle_endtag(self,t):
  n=self.cur
  while n.parent:
   if n.tag==t:self.cur=n.parent;return
   n=n.parent
 def handle_data(self,d):self.cur.children.append(d)
 def handle_entityref(self,n):self.cur.children.append('&'+n+';')
 def handle_charref(self,n):self.cur.children.append('&#'+n+';')

def retained_page(path):
 s=path.read_text(); parsed=Parser(s);main=next(n for n in parsed.root.walk() if n.tag=='main')
 for n in list(main.walk()):
  cl=n.attrs.get('class','').split();txt=n.text().lower()
  if any(x in cl for x in ['ph','helped','ba-grid','cta-band','for-you','habit']):n.remove();continue
  if n.tag=='section' and n.attrs.get('id') in ['hasil','testimoni','instagram']:n.remove();continue
  if n.tag=='article' and ('awaiting medical lead sign-off' in txt or 'menunggu persetujuan medical lead' in txt):n.remove();continue
  if n.tag=='span' and ('placeholder' in txt or 'shoot:' in txt):n.remove();continue
  n.attrs.pop('style',None)
  if n.tag=='img':n.attrs['loading']='lazy'
 # Replace the old title section with the new spacious masthead.
 h1=next((n for n in main.walk() if n.tag=='h1'),None)
 oldtitle=h1.text() if h1 else tr('Explore Surface','Jelajahi Surface')
 lead=next((n.text() for n in main.walk() if 'lead' in n.attrs.get('class','').split()),'')
 if h1:
  ancestor=h1
  while ancestor.parent and ancestor.parent!=main:ancestor=ancestor.parent
  ancestor.remove()
 html=''.join(x.html() if isinstance(x,Node) else x for x in main.children)
 html=html.replace('Clear, Glow, or Lift','one of our six skin pathways').replace('Clear, Glow, atau Lift','salah satu dari enam jalur kulit')
 return hero(tr('EXPLORE SURFACE','JELAJAHI SURFACE'),oldtitle,lead)+f'<div class="rebuilt-content" id="content">{html}</div>'

def home():
 body=hero(tr('DOCTOR-LED SKIN CARE · SINCE 2014','PERAWATAN BERSAMA DOKTER · SEJAK 2014'),tr('Your skin.<br>Your pace.<br><em>A better habit.</em>','Kulitmu.<br>Ritmemu.<br><em>Kebiasaan lebih baik.</em>'),tr('Thoughtful treatments. A plan that’s yours. Skin care that grows with you.','Perawatan terarah. Rencana milikmu. Perawatan kulit yang tumbuh bersamamu.'),'assets/clinics/tsm-resepsi.jpg')
 body=body.replace('href="#content"','href="#concern"').replace(tr('Explore below ↓','Jelajahi lebih lanjut ↓'),tr('Find your skin pathway ↓','Temukan jalur kulitmu ↓'))
 return body+'<div class="trust-strip"><span>'+tr('Free doctor consultation','Konsultasi dokter gratis')+'</span><span>'+tr('Four connected clinics','Empat klinik terhubung')+'</span><span>'+tr('Clear prices before treatment','Harga jelas sebelum treatment')+'</span></div>'+concerns()+approach()+team()+section('<div class="clinic-detail"><div class="clinic-image">'+img('assets/clinics/tsm-koridor.jpg',tr('Inside Surface TSM Cibubur','Interior Surface TSM Cibubur'))+'</div><div>'+label('YOUR NEIGHBOURHOOD SURFACE','SURFACE DI DEKATMU')+'<h2>'+tr('Four clinics.<br>One familiar feeling.','Empat klinik.<br>Satu rasa nyaman.')+'</h2><p>'+tr('Find your space to pause, ask questions, and care for your skin.','Temukan ruang untuk jeda, bertanya, dan merawat kulitmu.')+'</p><div class="clinic-list">'+''.join(link(c['short']+' ↗','klinik.html#'+c['code'].lower(),'') for c in C['clinics'])+'</div></div></div>')

def render(path,body,titletext,twin,interest=''):
 titletext=unescape(titletext)
 desc=re.sub('<[^>]*>','',titletext)+' · '+tr('Personalised doctor-led skin care at Surface Skin Habit.','Perawatan kulit personal bersama dokter di Surface Skin Habit.')
 prefix='../' if EN else ''
 twin_absolute=ORIGIN+'/'+(twin[3:] if EN and twin.startswith('../') else twin)
 html=f'''<!doctype html><html lang="{tr('en','id')}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(titletext)} · Surface Skin Habit</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow"><meta name="theme-color" content="#f8f5ef"><link rel="canonical" href="{ORIGIN}/{path.relative_to(OUT)}"><link rel="alternate" hreflang="{tr('id','en')}" href="{twin_absolute}"><meta property="og:title" content="{e(titletext)} · Surface Skin Habit"><meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{ORIGIN}/assets/logo-full.png"><link rel="icon" href="{prefix}assets/favicon.svg"><link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet"><link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/redesign.css"><link rel="stylesheet" href="{prefix}assets/full-site.css"><link rel="stylesheet" href="{prefix}assets/typography.css"></head><body data-locale="{tr('en','id')}">{header(twin)}<main id="main">{body}{booking(interest)}</main>{footer()}</body></html>'''
 # Version shared assets so existing visitors receive the matching styles and booking logic.
 for name in ['assets/style.css','assets/redesign.css','assets/full-site.css','assets/typography.css','assets/redesign.js','assets/analisis.js']:
  token=hashlib.sha256((OUT/name).read_bytes()).hexdigest()[:10]
  html=re.sub(re.escape(name)+r'(?:\?[^"]*)?(?=")',name+'?v='+token,html)
 path.parent.mkdir(exist_ok=True,parents=True);path.write_text(html)

# Match counterpart routes using the original hreflang declarations.
def twin_for(src):
 s=src.read_text();m=re.search(r'<link rel="alternate" hreflang="'+tr('id','en')+r'" href="([^"]+)"',s)
 if m:
  u=m[1].split('surfaceskinhabit.com/')[-1]
  return '../'+u if EN else u
 return '../index.html' if EN else 'en/index.html'

exec((ROOT/'site_features.py').read_text(),globals())
exec((ROOT/'skin_education.py').read_text(),globals())
route_count=0
for language in ['id','en']:
 EN=language=='en'; source=CONTENT/'legacy'/('en' if EN else '')
 for p in sorted(source.glob('*.html')):
  name=p.name;code=next((code for code,s in C['streams'].items() if name==field(s,'slug')+'.html'),None)
  aliases={'acne.html':'CLEAR','brightening.html':'TONE','firming.html':'TIGHTEN'}
  if EN and name in aliases:code=aliases[name]
  interest=code or ''; t=tr('Explore Surface','Jelajahi Surface')
  if name=='index.html':body=home()+faq(C['faq']).replace('class="section faq-section"','id="faq" class="section faq-section"');t=tr('Your skin. Your pace. A better habit.','Kulitmu. Ritmemu. Kebiasaan lebih baik.')
  elif code:body=programme(code);t=field(next(o for o in C['concerns'] if o['code']==code),'title')
  elif name=='dokter.html':body=doctors_page();t=tr('Our doctors','Dokter kami')
  elif name=='klinik.html':body=clinics_page();t=tr('Our clinics','Klinik kami')
  elif name=='menu.html':body=menu_page();t=tr('Treatments & prices','Treatment & harga')
  elif name=='edukasi-treatment.html':body=treatment_directory();t=tr('Treatment explainers','Penjelasan treatment')
  elif name=='edukasi.html':body=education_page();t=tr('Skin education','Edukasi kulit')
  elif name=='blog.html':body=blog_page();t=tr('The Surface Journal','Jurnal Surface')
  elif name=='metode.html':body=hero(tr('THE SURFACE APPROACH','PENDEKATAN SURFACE'),tr('Treatment is a habit.<br>Care is personal.','Treatment adalah kebiasaan.<br>Perawatan itu personal.'),tr('A doctor assessment, a clear plan, and reviews along the way.','Penilaian dokter, rencana yang jelas, dan tinjauan sepanjang perjalanan.'),'assets/clinics/tsm-koridor.jpg')+approach()+concerns();t=tr('The Skin Habit approach','Pendekatan Skin Habit')
  elif name=='cs.html':body=hero(tr('SURFACE HELP','BANTUAN SURFACE'),tr('Let’s make it clearer.','Mari pahami lebih jelas.'),tr('Answers to common questions about consultation, pricing, and your visit.','Jawaban untuk pertanyaan tentang konsultasi, harga, dan kunjunganmu.'))+faq(C['faq']).replace('class="section faq-section"','id="content" class="section faq-section"');t=tr('Help & questions','Bantuan & pertanyaan')
  elif name=='seo.html':body=hero(tr('EXPLORE SURFACE','JELAJAHI SURFACE'),tr('Find your way.','Temukan tujuanmu.'),tr('All the essentials, in one place.','Semua yang penting, dalam satu tempat.'))+concerns().replace('id="concern"','id="content"');t=tr('Explore Surface','Jelajahi Surface')
  elif name=='404.html':body=hero('404',tr('A little off track.','Sedikit keluar jalur.'),tr('This page could not be found. Find your way back to Surface.','Halaman ini tidak ditemukan. Kembali jelajahi Surface.'))+section(link(tr('Back to home ↗','Kembali ke beranda ↗'),'index.html','button'),id='content');t=tr('Page not found','Halaman tidak ditemukan')
  else:
   d=next((d for d in C['education']['devices'] if name=='edukasi-'+d['slug']+'.html'),None)
   post=next((x for x in C['posts'] if name=='blog-'+field(x,'slug')+'.html'),None)
   if d:body=device_page(d);t=d['name']
   elif post:body=blog_page(post);t=field(post,'title')
   else:
    body=retained_page(p);body=body.replace('id="content">','id="content"><p class="assessment-privacy">'+tr('Your answers stay in this browser until you choose to share your result on WhatsApp.','Jawabanmu tetap di browser ini sampai kamu memilih membagikan hasil melalui WhatsApp.')+'</p>',1) if name=='analisis.html' else body;h=re.search('<h1[^>]*>(.*?)</h1>',p.read_text(),re.S);t=re.sub('<[^>]*>','',h[1]) if h else t
  body=body.replace('href="#content"','href="#concern"') if name=='metode.html' else body
  render(OUT/('en' if EN else '')/name,body,t,twin_for(p),interest);route_count+=1
extra_routes()
# Backwards-compatible Indonesian homepage URL from the initial preview.
shutil.copy(OUT/'index.html',OUT/'id.html')
# Public sitemap for the GitHub Pages deployment.
urls=[ORIGIN+'/'+str(p.relative_to(OUT)) for p in [*OUT.glob('*.html'),*(OUT/'en').glob('*.html')] if p.name not in ['404.html','cs.html','seo.html','id.html']]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+u+'</loc></url>' for u in urls)+'</urlset>')
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nDisallow: /surface-skin-habit-website/content/\nSitemap: '+ORIGIN+'/sitemap.xml\n')
print(f'Rebuilt {route_count} routes plus Indonesian homepage alias.')

for language in ['id','en']:
 base=OUT/('en' if language=='en' else '')
 mapping={s['slug']+'.html':s['slug_en']+'.html' for s in C['streams'].values()}
 mapping.update({'blog-'+p['slug']+'.html':'blog-'+p['slug_en']+'.html' for p in C['posts']})
 for p in base.glob('*.html'):
  text=p.read_text()
  if language=='en':
   for old,new in mapping.items():text=text.replace('href="'+old,'href="'+new)
  text=text.replace('menu.html#enhance-correct','menu.html#enhance').replace('menu.html#enhance-refine','menu.html#enhance')
  for old in ['glass-skin-facial','acne-reset','glow-intensive','tone-reset','peel-and-lift','contour-signature','jawline-define']:
   text=text.replace('menu.html#'+old,'menu.html#stack')
  p.write_text(text)

# Load licensed webfonts only when supplied; no missing-font requests.
fontcss=OUT/'assets/typography.css'
fonts=fontcss.read_text()
fonts=re.sub(r",url\('fonts/Gotham-[^']+'\) format\('woff2'\)",'',fonts)
for style in ['Book','Medium','Bold']:
 filename='Gotham-'+style+'.woff2'
 if (OUT/'assets/fonts'/filename).exists():
  fonts=fonts.replace("local('Gotham-"+style+"')", "local('Gotham-"+style+"'),url('fonts/"+filename+"') format('woff2')")
fontcss.write_text(fonts)
