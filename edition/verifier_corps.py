"""Comparer le corps à l’épreuve 1ebaa3b, sans exclure le texte des tableaux."""
from collections import Counter
import re, sys, subprocess
import pymupdf as m
from pathlib import Path
baseline=m.open(sys.argv[1]) if len(sys.argv)>1 else m.open(stream=subprocess.check_output(['git','show','1ebaa3b:edition/Rapport_epreuve.pdf']),filetype='pdf')
final=m.open(Path(__file__).with_name('Rapport_epreuve.pdf'));assert len(final)==len(baseline)
def glyphes(p):
 n=p.number+1;res=Counter()
 for run in p.get_texttrace():
  for u,g,(x,y),box in run['chars']:
   # Only the running furniture and the explicitly changed display titles are exempt.
   if n>1 and (y<=55 or y>=p.rect.height-48):continue
   if n in [2,3,4,11,14,17,26,83,89,96,100] and y<=106 and run['size']>28:continue
   res[(u,re.sub(r'^[A-Z]{6}\+','',run['font']),round(run['size'],3),round(x,3),round(y,3),tuple(round(a,3) for a in box))]+=1
 return res
issues=[];count=0
for p,q in zip(baseline,final):
 a,b=glyphes(p),glyphes(q);count+=a.total()
 if a!=b:issues.append((p.number+1,(a-b).most_common(1),(b-a).most_common(1)))
assert not issues,issues[:8]
print(f'{len(final)} pages : {count} caractères identiques (texte, police, taille, origine et boîte).')
