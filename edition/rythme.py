"""Composer la prose dans ses plages réservées, sans modifier les objets voisins."""
from functools import lru_cache
from itertools import groupby

@lru_cache(None)
def mot_univers(word):
    # Use the actual em widths of the embedded Univers. Only missing glyphs use
    # a fallback face. The output is not stretched to the source's line width.
    k=choose(word)
    groups=[(k,word)] if k else [(key,''.join(chars)) for key,chars in groupby(word,key=lambda c:choose(c))]
    return [(fonts.get(key,backup[False]),v,fonts.get(key,backup[False]).text_length(v,fontsize=1)) for key,v in groups]

@lru_cache(None)
def avance(word):return sum(a for _,_,a in mot_univers(word))

def lignes_composees(paras,width,sz):
    groups=[]
    for para in paras:
        rows=[];row=[];width_used=0
        for word in para.split():
            ww=avance(word)*sz
            if ww>width:return []
            if row and width_used+avance(' ')*sz+ww>width:rows.append(row);row=[];width_used=0
            width_used+=ww+(avance(' ')*sz if row else 0);row.append(word)
        if row:rows.append(row)
        groups.append(rows)
    return groups

def plan_prose(page,blocks):
    schedule={};ignore=set();offset=0
    # Exclude tables, callouts and their cells even when they contain normal prose.
    obstacles=[z['rect'] for z in page.get_drawings() if z['fill'] and z['rect'].width>15 and z['rect'].height>4];obstacles += [m.Rect(im['bbox']) for im in page.get_image_info()]
    for block in blocks:
        lines=block['lines'];indices=[]
        for l in lines:
            ids=list(range(offset,offset+len(l['spans'])));indices.append(ids);offset+=len(ids)
        box=m.Rect(block['bbox']);n=page.number+1
        if n in [13,26] or box.x0<49 or box.x0>70 or box.width<310 or box.y0<57 or box.y1>799 or any(box.intersects(r) for r in obstacles):continue
        def suitable(l):
            ss=[v for v in l['spans'] if v['text'].strip()];return (ss and abs(l['bbox'][0]-box.x0)<2.2 and all(v['font'] in ['Aptos','Calibri'] and 10.4<=v['size']<=12.2 and v['color'] in [0,0x1f2a37] for v in ss))
        for ok,run in groupby(range(len(lines)),key=lambda j:bool(suitable(lines[j]))):
            js=list(run)
            if not ok or len(js)<2:continue
            X=box.x0;W=min(539-X,max(lines[j]['bbox'][2] for j in js)-X)
            if W<310:continue
            first,last=js[0],js[-1];top=lines[first]['bbox'][1];bottom=lines[last]['bbox'][3];paras=[''];old='';right=X+W
            for j in js:
                value=''.join(v['text'] for v in lines[j]['spans']).strip()
                if j!=first and lines[j-1]['bbox'][2]<right-8 and old.endswith(('.',':',';','!','?','»')):paras.append('')
                sep='' if paras[-1].endswith(('-','’',"'")) else ' ';paras[-1]=(paras[-1]+sep+value).strip();old=value
            if sum(len(t) for t in paras)<110:continue
            # Reserve a little extra air below an immediately preceding heading.
            # Dense passages trade leading for fit, never a collision with artwork.
            fit=None
            for size in [12,11.75,11.5,11.25,11]:
                rows=lignes_composees(paras,W,size);N=sum(map(len,rows));P=len(paras)-1
                if not rows or not N:continue
                y0=top+size+2.6;available=bottom-y0-size*.22
                lead=min(18,available/max(1,N-1+P*.48));gap=min(16, max(0,available-lead*(N-1))/max(P,1))
                if N==1 or lead>=size*1.19:
                    fit=(X,W,y0,size,lead,gap,rows);break
            if fit:
                ids=[idx for j in js for idx in indices[j]];schedule[ids[0]]=fit;ignore.update(ids[1:])
    return schedule,ignore

def poser_prose(p,item):
    X,W,Y,size,lead,gap,paragraphs=item;writer=m.TextWriter(p.rect)
    for rows in paragraphs:
        for j,row in enumerate(rows):
            space=avance(' ')*size
            if j+1<len(rows) and len(row)>1:space=(W-size*sum(avance(word) for word in row))/(len(row)-1)
            x=X
            for word in row:
                for font,chunk,a in mot_univers(word):
                    writer.append((x,Y),chunk,font=font,fontsize=size);x+=a*size
                x+=space
            Y+=lead
        Y+=gap
    writer.write_text(p,color=ink)
