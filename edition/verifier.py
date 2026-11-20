"""Contrôles de l'épreuve, à lancer depuis la racine."""
import glob,collections,re,unicodedata,json
from pathlib import Path
import pymupdf as m
s=m.open(glob.glob('Rapport_Diagnostic*.pdf')[0]);d=m.open('edition/Rapport_epreuve.pdf');assert len(s)==len(d)==151
fig=[27,29,34,35,36,37,38,43,44,48,49,51,52,53,54,58,61,63,68,77,81]
records=json.loads(Path("edition/zones_design.json").read_text())
def content(page,exclude=None):
 extra=[m.Rect(r["zone"]) for r in records if page.parent is d and r["page"]==page.number+1]
 groups=[]
 for b in page.get_text('dict',flags=0)['blocks']:
  for l in b['lines']:
   for z in l['spans']:
    if any(area.contains(m.Point(z["origin"])) for area in extra):continue
    if exclude and exclude.intersects(m.Rect(z['bbox'])):continue
    groups.append(z['text'])
 return ''.join(groups)
def norm(t):return ''.join(unicodedata.normalize('NFKC',t.replace('\uf0b7','•')).split())
issues=[];overflow=[]
for p,q in zip(s,d):
 n=p.number+1;im=m.Rect(p.get_image_info()[0]['bbox']) if n in fig else None
 if im:assert not q.get_image_info(),n
 pix=q.get_pixmap(matrix=m.Matrix(.5,.5),colorspace=m.csGRAY);assert min(pix.samples)<160,n
 if n not in [4,5,6,7,8]:
  a=norm(content(p));b=norm(content(q,im));
  if a!=b:issues.append((n,len(a),len(b),''.join((collections.Counter(a)-collections.Counter(b)).elements())[:40]))
 for w in q.get_text('words'):
  if not q.rect.contains(m.Rect(w[:4])):overflow.append((n,w[4]))
print('Pages rendues :',len(d),' ; figures sans image matricielle :',len(fig));print('Écarts de flux textuel hors sommaire et graphiques :',issues);print('Mots hors page :',overflow[:50]);print('Signets :',len(d.get_toc()))
assert not issues and not overflow
flat=lambda t:''.join(c for c in unicodedata.normalize('NFKD',t.lower()) if c.isalnum())
for level,title,n in d.get_toc():assert flat(title) in flat(d[n-1].get_text()),(title,n)
assert sum(len(d[i].get_links()) for i in [3,4])==len(d.get_toc())
print('Chaque entrée du sommaire correspond à un titre présent sur la page indiquée.')
# Reconcile all contents entries with the printed source, including the targets.
source_toc=[]
for i in [3,4]:
 body=s[i].get_text().split(f'\n{i+1} \n',1)[1].replace('Table des matières','')
 for item in re.finditer(r'(.+?)\.{2,}\s*(\d+)\s*(?:\n|$)',body,re.S):source_toc.append((norm(item[1]),int(item[2])))
assert [(norm(t),n) for _,t,n in d.get_toc()]==source_toc
for i,group in zip([3,4],[source_toc[:28],source_toc[28:]]):
 links=sorted(d[i].get_links(),key=lambda a:a['from'].y0);assert [a['page']+1 for a in links]==[n for _,n in group]
 assert all(t in norm(content(d[i])) for t,_ in group)
# The index was reconstructed from the printed list, reconciled with each caption.
from index_listes import lire_listes
catalog=list(lire_listes(s));assert len(catalog)==122
for n in [6,7,8]:
 q=d[n-1];items=[r for r in catalog if r[0]==n];links=sorted(q.get_links(),key=lambda a:a['from'].y0)
 assert not q.get_image_info() and len(items)==len(links)
 for (_,kind,num,title,pg),ln in zip(items,links):
  assert pg and ln['page']==pg-1,(kind,num,pg)
  value=norm(kind+' '+num+':'+title)
  assert value in norm(s[pg-1].get_text()) and str(pg)+value in norm(content(q)),(n,num,pg,title)
print('122 intitulés des listes et leurs destinations validés ; tableau 29 : page 70.')
assert sorted(im['digest'] for im in s[0].get_image_info(hashes=True))==sorted(im['digest'] for im in d[0].get_image_info(hashes=True))
import csv
with open('edition/Controle_par_page.csv','w',encoding='utf-8-sig',newline='') as f:
 out=csv.writer(f,delimiter=';');out.writerow(['Page source','Page épreuve','Comparaison','Rendu non blanc','Mots hors page','Figure vectorielle'])
 for n in range(1,len(d)+1):
  how='Sommaire : intitulés, destinations, liens' if n in [4,5] else 'Liste : légendes et destinations réconciliées' if n in [6,7,8] else 'Flux de texte normalisé, hors zone de figure' if n in fig else 'Texte et trois logos' if n==1 else 'Flux de texte normalisé'
  out.writerow([n,n,how,'Oui',0,fig.index(n)+1 if n in fig else ''])

# Control the actual text of every new editorial layer independently, not just the source flow.
for r in records:
 n=r['page'];q=d[n-1];area=m.Rect(r['zone']);words=norm(q.get_text(clip=area));src=norm(s[n-1].get_text())
 if r['type']=='navigation':
  assert norm(r['titre'])+str(n)==words,(n,words)
 elif r['type']=='lecture':
  assert words==norm(''.join(r['libelles'])),(n,words)
  if n==23:
   for j in range(4,len(r['libelles']),2):
    label,nums=r['libelles'][j:j+2];assert norm(label) in src and norm(nums.replace('/','')) in src,(n,label,nums)
  else:
   for label in r['libelles']:
    assert norm(label).casefold() in src.casefold(),(n,label)
 else:
  assert norm(r['province']) in words and norm(r['province']) in src
  for value in r['valeurs']:assert norm(value+' %') in words and norm(value+' %') in src,(n,value)
  if area.height>=134:
   for v in [r['evaluation']+' évaluations calculables',r['etablissements']+' établissements',r['zones']+' zones']:assert norm(v) in src and norm(v) in words,(n,v)
assert len([r for r in records if r['type']=='navigation'])==150
assert len([r for r in records if r['type']=='profil'])==8
print('Navigation contrôlée sur 150 pages intérieures ; huit comparaisons provinciales rapprochées de leur texte source.')
