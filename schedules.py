"""Doctor schedules by day and clinic (Steve, 23 Oct 2026). Derived from attendance; marked unverified until managers confirm."""
DAY_EN={'Mon':'Mon','Tue':'Tue','Wed':'Wed','Thu':'Thu','Fri':'Fri','Sat':'Sat','Sun':'Sun'}
DAY_ID={'Mon':'Sen','Tue':'Sel','Wed':'Rab','Thu':'Kam','Fri':'Jum','Sat':'Sab','Sun':'Min'}
ORDER=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
def clinic_short(code):return next(x['short'] for x in C['clinics'] if x['code']==code)
def sched_note():
 return '<p class="sched-note">'+tr('Regular days, not a guarantee: doctors also work by appointment and schedules shift. We confirm the doctor when you book.','Hari rutin, bukan jaminan: dokter juga praktik sesuai janji dan jadwal bisa bergeser. Kami konfirmasi dokternya saat kamu booking.')+'</p>'
def day_strip(days):
 return '<ul class="day-strip" aria-label="'+tr('Days','Hari')+'">'+''.join('<li class="'+('on' if d in days else '')+'"><abbr title="'+d+'">'+(DAY_EN if EN else DAY_ID)[d]+'</abbr></li>' for d in ORDER)+'</ul>'
def doctor_schedule(d):
 rows=''
 for s in d.get('schedule',[]):
  if s.get('days'):rows+='<div class="sched-row"><b>'+e(clinic_short(s['clinic']))+'</b>'+day_strip(s['days'])+'</div>'
  else:rows+='<div class="sched-row"><b>'+e(clinic_short(s['clinic']))+'</b><span class="small">'+tr('By appointment','Sesuai janji')+'</span></div>'
 if not rows:return ''
 return '<div class="doctor-schedule"><span class="kicker">'+tr('WHERE AND WHEN','DI MANA DAN KAPAN')+'</span>'+rows+'</div>'
_sched_doctor_cards=doctor_cards
def doctor_cards(full=False):
 body=_sched_doctor_cards(full)
 for d in C['doctors']:
  if not d.get('publish') or not d.get('schedule'):continue
  anchor='id="doctor-'+d['name'].split()[1].lower()+'"'
  i=body.find(anchor)
  if i<0:continue
  j=body.find('</div></article>',i)
  if j<0:continue
  body=body[:j]+doctor_schedule(d)+body[j:]
 if full:body+=sched_note()
 return body
def clinic_doctor_days(c):
 items=''
 for d in C['doctors']:
  if not d.get('publish'):continue
  for s in d.get('schedule',[]):
   if s['clinic']!=c['code']:continue
   items+='<li><a href="dokter.html#doctor-'+d['name'].split()[1].lower()+'">'+e(d['name'])+'</a>'+(day_strip(s['days']) if s.get('days') else '<span class="small">'+tr('By appointment','Sesuai janji')+'</span>')+'</li>'
 extra=C.get('schedule_meta',{}).get('clinic_doctor_days',{}).get(c['code'])
 if extra and not items:items+='<li><span>'+tr('Doctor on duty','Dokter jaga')+'</span>'+day_strip(extra)+'</li>'
 if not items:return ''
 return '<div class="clinic-doctors"><span class="kicker">'+tr('DOCTOR DAYS','HARI DOKTER')+'</span><ul>'+items+'</ul>'+sched_note()+'</div>'
_sched_clinics_page=clinics_page
def clinics_page():
 body=_sched_clinics_page()
 for c in C['clinics']:
  needle='<h2>'+e(c['name'])+'</h2><p>'+e(c['address'])+'</p>'
  body=body.replace(needle,needle+clinic_doctor_days(c),1)
 return body
