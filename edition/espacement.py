"""Espacement vertical exprimé en points PDF (96 pixels CSS pour 72 points)."""
from collections import Counter
mesures_espaces=Counter()

ESPACE = 6 * 72 / 96

def regler_espaces(page,blocks,spans,headings,skip,prose,ignored):
    n=page.number+1
    if n in (13,26):return {},{}
    # Paragraphs and titles are rigid boxes: change only their baseline offsets,
    # not the previously fitted font, width, line breaks or leading.
    runs=[];offsets={};paragraphs={};used=set(skip)|set(ignored)
    for k,(x,w,y,sz,lead,_,pars) in prose.items():
        paragraphs[k]=[];used.add(k)
        for rows in pars:
            height=sz+(len(rows)-1)*lead
            runs.append([y-.8*sz,y-.8*sz+height,'p',k,len(paragraphs[k])]);paragraphs[k].append(y)
            y+=len(rows)*lead+prose[k][5]
    fixed=[]
    for k,(_,y,_,sz,*_) in headings.items():
        used.add(k)
        if sz>=30:fixed.append((45,90 if n!=9 else 83));continue
        runs.append([y-.8*sz,y+.2*sz,'h',k,None]);offsets[k]=0
    # Plain paragraphs that had not been line-wrapped (short or mixed-weight).
    idx=0
    for b in blocks:
        ss=[s for l in b['lines'] for s in l['spans']];ids=[idx+j for j,s in enumerate(ss) if s['text'].strip()];idx+=len(ss)
        if not ids or any(i in used for i in ids):continue
        r=m.Rect(b['bbox']);s0=spans[ids[0]]
        if r.y0<58 or r.y1>788 or abs(r.x0-56.7)>1 or r.width<210 or not all('Aptos' in spans[i]['font'] and 10.4<=spans[i]['size']<=12.2 for i in ids):continue
        if n in TABLEAUX and r.intersects(m.Rect(TABLEAUX[n][0][0],TABLEAUX[n][1][0],TABLEAUX[n][0][-1],TABLEAUX[n][1][-1])):continue
        if any(r.intersects(m.Rect(z['rect'])) for z in page.get_drawings() if z['fill'] and z['rect'].width>16 and z['rect'].height>4):continue
        top=min(spans[i]['origin'][1]-.8*spans[i]['size'] for i in ids);bot=max(spans[i]['origin'][1]+.2*spans[i]['size'] for i in ids)
        runs.append([top,bot,'r',tuple(ids),None]);used.update(ids)
    for i,s in enumerate(spans):
        if i not in used and s['text'].strip() and 55<s['origin'][1]<790:fixed.append((s['bbox'][1],s['bbox'][3]))
    for im in page.get_image_info():fixed.append((im['bbox'][1],im['bbox'][3]))
    for z in page.get_drawings():
        r=z['rect'];c=z['fill']
        if c and r.width>16 and r.height>4 and min(c)<.98:fixed.append((r.y0,r.y1))
    # Reserve any charts added below the original body.
    ends={23:564,55:285,64:604};limit=ends.get(n,790)
    if n in (100,105,110,115,119,124,129,134):limit=max(b[3] for b in page.get_text('blocks') if b[1]<785 and b[4].strip())+14
    fixed.extend([(0,46),(limit,page.rect.height)])
    def fusion(zones):
        merged=[]
        for a,b in sorted(zones):
            if merged and a<=merged[-1][1]:merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
            else:merged.append((a,b))
        return merged
    merged=fusion(fixed)
    # A paragraph or caption straddling a locked element is itself an obstacle.
    while True:
        locked=[r for r in runs if any(a<r[1]-.2 and b>r[0]+.2 for a,b in merged)]
        if not locked:break
        merged=fusion(merged+[(r[0],r[1]) for r in locked]);runs=[r for r in runs if r not in locked]
    for (_,lo),(hi,_) in zip(merged,merged[1:]):
        group=sorted((r for r in runs if lo-.2<=r[0] and r[1]<=hi+.2),key=lambda r:r[0]);
        if not group:continue
        total=sum(r[1]-r[0] for r in group);room=hi-lo-total
        # If abutting locked artwork leaves too little room, retain the largest
        # possible common gap rather than modifying the line spacing or the chart.
        gap=min(ESPACE, max(0,room/(len(group)+1)));height=total+gap*(len(group)-1)
        mesures_espaces['normal' if gap==ESPACE else 'contraint']+=len(group)
        start=max(lo+gap,min(group[0][0],hi-gap-height))
        if group[0][2]=='h' or (lo>46 and group[0][0]-lo<30):start=lo+gap
        for a,b,kind,k,j in group:
            diff=start-a
            if kind=='p':paragraphs[k][j]+=diff
            elif kind=='r':offsets.update({i:diff for i in k})
            else:offsets[k]=diff
            start+=b-a+gap
    return offsets,paragraphs
