from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import re,json
R=Path(__file__).parent
class Page(HTMLParser):
 def __init__(self,s):super().__init__();self.links=[];self.ids=[];self.h1=0;self.feed(s)
 def handle_starttag(self,t,a):
  a=dict(a)
  if t=='h1':self.h1+=1
  if a.get('id'):self.ids.append(a['id'])
  for k in ['href','src']:
   if a.get(k):self.links.append((t,k,a[k]))
pages={p:Page(p.read_text()) for p in [*R.glob('*.html'),*(R/'en').glob('*.html')]};issues=[]
for p,data in pages.items():
 if data.h1!=1:issues.append((str(p.relative_to(R)),'h1',data.h1))
 for t,k,url in data.links:
  u=urlsplit(url)
  if u.scheme or u.netloc:continue
  dest=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
  if dest.is_dir():dest=dest/'index.html'
  if not dest.exists():issues.append((str(p.relative_to(R)),'missing',url))
  elif u.fragment and dest.suffix=='.html':
   target=next((x for x in pages if x.resolve()==dest),None)
   if target and unquote(u.fragment) not in pages[target].ids:issues.append((str(p.relative_to(R)),'anchor',url))
 if len(data.ids)!=len(set(data.ids)):issues.append((str(p.relative_to(R)),'duplicate id',''))
 if re.search(r'SHOOT:|Design placeholder|Placeholder desain|awaiting Medical Lead|menunggu persetujuan Medical Lead',p.read_text(),re.I):issues.append((str(p.relative_to(R)),'draft copy',''))
print(json.dumps({'pages':len(pages),'issues':issues},indent=2))
raise SystemExit(bool(issues))
