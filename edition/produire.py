"""Depuis la racine du dépôt : python edition/produire.py (PyMuPDF, fonttools)."""
import io,re,glob,collections
from pathlib import Path
import pymupdf as m
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import CmapSubtable
R=m.open('Md_ref.pdf'); S=m.open(glob.glob('Rapport_Diagnostic*.pdf')[0]); D=m.open(S.name)
OUT=Path('edition'); green=(.102,.337,.196); gold=(.79,.61,.27); ink=(.137,.122,.125); white=(1,1,1)
# Recover Unicode mapping of the embedded symbol-encoded font subsets, using glyphs actually printed.
fonts={}; used={}; families=collections.defaultdict(dict)
for p in R:
 names=collections.defaultdict(list)
 for x,ext,_,base,*_ in p.get_fonts():
  if ext=='ttf' and 'Univers' in base:names[base.split('+')[-1]].append(x)
 for name,xs in names.items():
  for x in set(xs):
   if x in fonts:continue
   t=TTFont(io.BytesIO(R.extract_font(x)[3]))
   if 'cmap' not in t:continue
   cm=t['cmap'].tables; mac=next((c.cmap for c in cm if c.platformID==1),{}); mapping={ord(bytes([k]).decode('mac_roman')):g for k,g in mac.items() if k<256};
   if not mapping:continue
   sub=CmapSubtable.newSubtable(4);sub.platformID=3;sub.platEncID=1;sub.language=0;sub.cmap=mapping;t['cmap'].tables=[sub];buf=io.BytesIO();t.save(buf);fonts[x]=m.Font(fontbuffer=buf.getvalue());used[x]=buf.getvalue();families['b' if 'Bold' in name else 'r'][x]=set(mapping)

def choose(text,bold=False):
 cs=set(map(ord,text)); pool=families['b' if bold else 'r'];return next((x for x in sorted(pool,key=lambda i:-len(pool[i])) if cs<=pool[x]),None)
cache={}
def text(p,x,y,t,size=10,col=ink,b=False,width=None,align='left'):
 if not t.strip():return
 key=(t,b); k=cache.get(key,-1)
 if k==-1:k=cache[key]=choose(t,b)
 if k is None:
  # Only missing glyphs use the fallback. Do not switch a whole French paragraph
  # to another family because a single accent is absent in the reference subset.
  pool=families['b' if b else 'r'];primary=max(pool,key=lambda f:sum(ord(c) in pool[f] for c in t));supported=pool[primary]
  if any(ord(c) in supported for c in t) and any(ord(c) not in supported for c in t):
   from itertools import groupby
   chunks=[''.join(g) for _,g in groupby(t,key=lambda c:ord(c) in supported)];widths=[fonts.get(choose(v,b),backup[b]).text_length(v,fontsize=size) for v in chunks];total=sum(widths);goal=width or total
   if align=='right':x-=goal
   elif align=='center':x-=goal/2
   for v,ww in zip(chunks,widths):
    ww=ww*goal/total;text(p,x,y,v,size,col,b,ww);x+=ww
   return
  name='FallbackB' if b else 'FallbackR';path='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf';font=backup[b];p.insert_font(fontname=name,fontfile=path)
 else:name='U'+str(k);font=fonts[k];p.insert_font(fontname=name,fontbuffer=used[k])
 w=font.text_length(t,fontsize=size);w2=width or w
 if align=='right':x-=w2
 if align=='center':x-=w2/2
 pt=m.Point(x,y);p.insert_text(pt,t,fontname=name,fontsize=size,color=col,morph=(pt,m.Matrix(w2/w,1)) if w and width else None)
backup={b:m.Font(fontfile='/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf') for b in [True,False]}
def rect(p,box,c):p.draw_rect(box,color=None,fill=c)
def line(p,x,y,X,Y,c,w=.5):p.draw_line((x,y),(X,Y),color=c,width=w)
def wrap(p,t,x,y,width,size,c,align='left',gap=1.14):
 words=t.split();rows=[''];
 for word in words:
  v=(rows[-1]+' '+word).strip();k=choose(v);f=fonts.get(k,backup[False]);
  if rows[-1] and f.text_length(v,fontsize=size)>width:rows.append(word)
  else:rows[-1]=v
 for row in rows:text(p,x,y,row,size,c,align=align);y+=size*gap
 return y
# Source pagination stays fixed. Replace the cover artwork, retaining all three authorised marks.
p=D[0];orig=S[0]
for x in p.get_contents():D.update_stream(x,b'')
rect(p,p.rect,green);rect(p,(0,0,595.32,110),white)
for i,im in enumerate(orig.get_image_info(xrefs=True)):
 box=[(442,27,555,83),(248,31,419,81),(42,27,225,83)][i];p.insert_image(box,xref=im['xref'])
line(p,547,365,547,779,gold,1);lines=[z.strip() for z in orig.get_text().splitlines() if z.strip()];wrap(p,' '.join(lines[:-1]),521,403,445,33,white,'right');text(p,521,752,lines[-1],20,gold,align='right')
# Recompose contents with the page-number column on the left, as in Md_ref.
entries=[]
for i in [3,4]:
 body=S[i].get_text().split(f'\n{i+1} \n',1)[1].replace('Table des matières','');start=len(entries)
 for match in re.finditer(r'(.+?)\.{2,}\s*(\d+)\s*(?:\n|$)',body,re.S):
  label=' '.join(match[1].split());num=int(match[2]);level=2 if re.match(r'(?:\d+\.|Annexe \d)',label) else 1;entries.append((level,label,num))
# Distribute entries over the two existing contents pages instead of crowding the first.
for i,group in [(3,entries[:28]),(4,entries[28:])]:
 p=D[i];
 for link in p.get_links():p.delete_link(link)
 for x in p.get_contents():D.update_stream(x,b'')
 text(p,56,44,'ICHESS, LLC',12,green,True);text(p,539,44,'International Center for Health Systems Strengthening',9,ink,align='right');line(p,56,54,539,54,green)
 if i==3:text(p,56,105,'Table des matières',32,green)
 y=142 if i==3 else 90;line(p,99,y-12,99,y+len(group)*19,(.84,.87,.84))
 for lvl,title,num in group:
  if lvl==1:line(p,111,y-13,539,y-13,(.89,.91,.88))
  text(p,89,y,str(num),10,green,align='right');x=113 if lvl==1 else 127;f=fonts.get(choose(title,lvl==1),backup[lvl==1]);w=f.text_length(title,fontsize=10.3);text(p,x,y,title,10.3,green if lvl==1 else ink,lvl==1,width=min(w,537-x));p.insert_link(dict(kind=m.LINK_GOTO,**{"from":m.Rect(59,y-12,537,y+3)},page=num-1,to=m.Point(0,0)));y+=19
 text(p,537,813,str(i+1),10,green,align='right')
D.set_toc(entries)
# Source drawings and chart locations remain untouched except for explicitly redrawn figures.
# Change the presentation colours, never the semantic red/yellow/green values.
colors={b'0.0431 0.157 0.282':b'0.102 0.337 0.196',b'0.788 0.827 0.871':b'0.831 0.862 0.844',b'0.957 0.969 0.98':b'0.959 0.972 0.962',b'0.227 0.486 0.133':b'0.102 0.337 0.196',b'0.122 0.165 0.216':b'0.137 0.122 0.125'}
for i in range(1,len(D)):
 if i in (3,4,5,6,7):continue
 p=D[i];src=S[i];
 for x in p.get_contents():
  data=D.xref_stream(x)
  for old,new in colors.items():data=data.replace(old+b' rg',new+b' rg').replace(old+b' RG',new+b' RG')
  D.update_stream(x,data)
 # Typeset body pages in the model's typefaces; retain the precision of dense matrices
 # and lists with embedded glyph-images in their native positioned text.

 spans=[s for block in src.get_text('dict',flags=0)['blocks'] for ln in block['lines'] for s in ln['spans']];
 for x in p.get_contents():
  raw=D.xref_stream(x);raw=re.sub(rb'/Artifact\s*<<[^>]*?/Subtype/(?:Header|Footer)[^>]*?>>\s*BDC\b.*?\bEMC\b',b'',raw,flags=re.S);D.update_stream(x,re.sub(rb'\bBT\b.*?\bET\b',b'',raw,flags=re.S))
 line(p,56,45,p.rect.width-56,45,(.82,.85,.83),.4)
 for s in spans:
  val=s['text'].rstrip().replace('\uf0b7','•');
  if not val.strip():continue
  x,y=s['origin'];w=s['bbox'][2]-x;oldsize=s['size'];col=tuple(v/255 for v in m.sRGB_to_rgb(s['color']));
  if s['color'] in (0,0x1f2a37):col=ink
  if s['color']==0x3a7c22 or (y<50 and len(val)>3):col=green
  if y<45 and 'ICHESS' in val:oldsize=8;w=None;x=78;y=37
  elif y<60 and 'International Center' in val:oldsize=8;w=None;x=139;y=37
  elif y>785 and val.strip()==str(i+1):oldsize=8;w=None;x=56;y=37;col=green
  elif s['text']!=val:w*=len(val)/len(s['text'])
  text(p,x,y,val,oldsize,col,'Bold' in s['font'],w)

exec((OUT/'figures.py').read_text())
D.subset_fonts();D.save(OUT/'Rapport_epreuve.pdf',garbage=4,deflate=True)
