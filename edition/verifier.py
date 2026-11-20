"""Contrôles de l'épreuve, à lancer depuis la racine."""
import glob,collections,re,unicodedata
import pymupdf as m
s=m.open(glob.glob('Rapport_Diagnostic*.pdf')[0]);d=m.open('edition/Rapport_epreuve.pdf');assert len(s)==len(d)==151
fig=[27,29,34,35,36,37,38,43,44,48,49,51,52,53,54,58,61,63,68,77,81]
def content(page,exclude=None):
 groups=[]
 for b in page.get_text('dict',flags=0)['blocks']:
  for l in b['lines']:
   for z in l['spans']:
    if exclude and exclude.intersects(m.Rect(z['bbox'])):continue
    groups.append(z['text'])
 return ''.join(groups)
def norm(t):return ''.join(unicodedata.normalize('NFKC',t.replace('\uf0b7','•')).split())
issues=[];overflow=[]
for p,q in zip(s,d):
 n=p.number+1;im=m.Rect(p.get_image_info()[0]['bbox']) if n in fig else None
 if im:assert not q.get_image_info(),n
 pix=q.get_pixmap(matrix=m.Matrix(.5,.5),colorspace=m.csGRAY);assert min(pix.samples)<160,n
 if n not in [4,5]:
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
