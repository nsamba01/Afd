"""Gabarit des titres et infographies : toutes les chaînes proviennent du diagnostic."""
def extent(t,size,bold=False):
    k=choose(t,bold)
    return fonts.get(k,backup[bold]).text_length(t,fontsize=size)

def cover_titles(p,lines):
    # Md_ref, couverture : Univers condensée 50/55, blanc ; date or 40 pt.
    # Le titre français est plus long : le bloc monte, sa dernière ligne reste ancrée.
    title=' '.join(lines[:-1]);rows=[''];width=465
    for word in title.split():
        trial=(rows[-1]+' '+word).strip()
        # Mesure de la majorité des glyphes dans Univers, même avec un accent absent.
        if rows[-1] and sum(extent(c,50) for c in trial)>width:rows.append(word)
        else:rows[-1]=trial
    end=685;start=end-55*(len(rows)-1)
    assert start>165
    line(p,539,start-48,539,767,(180/255,162/255,105/255),.85)
    for j,row in enumerate(rows):
        w=min(width,sum(extent(c,50) for c in row));text(p,512,start+55*j,row,50,white,width=w,align='right')
    text(p,512,760,lines[-1],40,(180/255,162/255,105/255),width=min(width,sum(extent(c,40) for c in lines[-1])),align='right')

def local_headings(spans,n):
    # Layout by baseline rather than enlarging isolated runs (numbers and titles
    # are often separate source spans). All intervening whitespace is typographic.
    lines={}
    for idx,s in enumerate(spans):
        if s['text'].strip():lines.setdefault(round(s['origin'][1],1),[]).append((idx,s))
    replacements={};skip=set()
    for y,runs in lines.items():
        runs.sort(key=lambda it:it[1]['origin'][0]);s=runs[0][1];t=' '.join(z['text'].strip() for _,z in runs);x=s['origin'][0]
        major=(n in [2,3,9,11,14,17,26,83,89,96,100] and 60<y<95 and s['size']>=17)
        sub=(re.match(r'^\d+\.\d+(?:\.|\s)',t) and 'Bold' in s['font'] and x<90 and s['size']>=11)
        if n in [11,12] and not major and 60<y<780 and x<70 and all('Bold' in z['font'] for _,z in runs):sub=True
        if not major and not sub:continue
        size=40 if major else (18 if s['size']>=12.5 else 14)
        # Multiline subsections must not grow into their continuation or preceding line.
        if not major:
            above=max([a for a in lines if a<y] or [45]);size=min(size,max(s['size'],y-above-1))
        x=56.7 if major else x
        w=min(539-x,sum(extent(c,size,not major) for c in t))
        if major and n==83:size=34;w=min(539-x,sum(extent(c,size) for c in t))
        # Give visible breathing room below a subtitle while keeping clear of the preceding line.
        if not major and (y-above)>size+5:y-=2.5
        replacements[runs[0][0]]=(x,y,t,size,green,not major,w);skip.update(i for i,_ in runs[1:])
    return replacements,skip

def results_infographic(p,src):
    # Composer directement la phrase d'échantillonnage : pas de résumé ajouté.
    raw=' '.join(src.get_text().split());lead,rest=raw.split('L’étude a porté sur ',1)
    parts=re.fullmatch(r'(160) (établissements) (répartis dans 40 zones de santé et huit provinces :) (101) (centres de santé,) (22) (centres de santé de référence et) (37) (hôpitaux généraux de référence\.)(.*)',rest)
    assert parts;total,unit,coverage,*detail=parts.groups();tail=detail.pop().strip();xs=57;right=538
    rect(p,(xs,244,right,365),green);text(p,77,268,'L’étude a porté sur',14,white);text(p,76,321,total,54,white);text(p,179,316,unit,29,white);text(p,78,347,coverage,14,white)
    for j,(count,label) in enumerate(zip(detail[::2],detail[1::2])):
        y=395+j*46;text(p,xs,y,count,21,green,True);text(p,105,y,label,15,ink);line(p,105,y+10,right,y+10,(.88,.91,.88),3);line(p,105,y+10,105+(right-105)*int(count)/int(total),y+10,green,3)
    # Join the line break after the genuine hyphen in the provincial name.
    words=tail.replace('Haut- Katanga','Haut-Katanga').split();rows=[[]];width=right-xs
    measure=lambda word:sum(extent(c,12) for c in word)
    for word in words:
        if rows[-1] and measure(' '.join(rows[-1]+[word]))>width:rows.append([])
        rows[-1].append(word)
    for j,row in enumerate(rows):
        y=546+16*j;x=xs;lengths=[measure(word) for word in row]
        gap=(width-sum(lengths))/(len(row)-1) if j<len(rows)-1 and len(row)>1 else measure(' ')
        for word,length in zip(row,lengths):
            text(p,x,y,word,12,ink,width=length);x+=length+gap

def status_band(p,src):
    # Une seule barre commune sous les trois cartes correspondantes, sans nouvel indicateur.
    vals=re.findall(r'(68,4|30,2|1,4) %\s+Fonctions (rouges|jaunes|vertes)',src.get_text());assert len(vals)==3
    x=252;w=286
    for (v,_),c in zip(vals,[(.72,.19,.22),(.95,.73,.13),green]):
        end=x+w*float(v.replace(',','.'))/100;rect(p,(x,779,end,785),c);x=end
