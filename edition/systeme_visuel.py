"""Éléments éditoriaux continus et infographies. Appelé par produire.py."""
import math,json
pine=(.075,.255,.17);mint=(.87,.93,.88);paper=(.95,.97,.94);ochre=(.70,.63,.41);brick=(.68,.20,.22)

def polygon(p,pts,fill):
    sh=p.new_shape();sh.draw_polyline(pts);sh.finish(fill=fill,color=None,closePath=True);sh.commit()

def pictogram(p,x,y,k,r=17):
    # Five line pictograms, built from paths, not font characters.
    p.draw_circle((x,y),r,fill=green,color=None)
    def edge(a,b):line(p,x+a[0],y+a[1],x+b[0],y+b[1],white,1.3)
    def node(a):p.draw_circle((x+a[0],y+a[1]),2.3,color=white,fill=green,width=1.2)
    if k==0:
        v=[(0,-7),(-8,6),(8,6)];[edge(v[i],v[(i+1)%3]) for i in range(3)];[node(a) for a in v]
    elif k==1:
        for j,h in enumerate([5,10,16]):rect(p,(x-8+j*6,y+7-h,x-5+j*6,y+7),white)
    elif k==2:
        p.draw_circle((x,y),8,color=white,width=1);edge((-5,0),(-1,4));edge((-1,4),(6,-4))
    elif k==3:
        for a,b in [((-8,-2),(0,-8)),((0,-8),(8,-2)),((-7,6),(7,6)),((-5,-1),(-5,5)),((0,-1),(0,5)),((5,-1),(5,5))]:edge(a,b)
    else:
        for a in [(-7,-6),(7,-6),(0,7)]:edge((0,0),a);node(a)

def prose(p,t,x,y,w,sz,lead,col=ink,b=False):
    def length(t):return sum(extent(c,sz,b) for c in t)
    rows=[''];
    for word in t.split():
        v=(rows[-1]+' '+word).strip()
        if rows[-1] and length(v)>w:rows.append(word)
        else:rows[-1]=v
    for j,row in enumerate(rows):text(p,x,y+j*lead,row,sz,col,b,width=min(w,length(row)))
    return y+len(rows)*lead

def recommendations(p,src):
    raw=' '.join(src.get_text().split()).split(' 13 ',1)[1];title,body=raw.split('Cinq messages',1);intro,rest=('Cinq messages'+body).split(' Le premier',1);parts=re.split(r' (?=Le (?:deuxième|troisième|quatrième|cinquième) est de )','Le premier'+rest);parts[-1],tail=parts[-1].split(' Ces constats',1);assert len(parts)==5
    rect(p,(56,58,539,167),green);rect(p,(56,58,61,167),ochre);prose(p,title,75,89,445,21,24,white);text(p,57,199,intro,16,green,True)
    line(p,76,224,76,623,mint,2)
    for j,para in enumerate(parts):
        y=220+j*91;rect(p,(103,y,539,y+82),paper if j%2==0 else (.976,.980,.967));pictogram(p,76,y+26,j)
        end=prose(p,para,116,y+19,410,12,14,ink);assert end<=y+93,(j,end)
    line(p,56,686,539,686,ochre);prose(p,'Ces constats'+tail,57,709,479,12,15)

def backdrop(p,n):
    # The long French title occupies the right of the cover. Set the geometry
    # UNDER its letters, like the reference's monochrome cover field.
    if n!=1:return
    rect(p,(0,111,595.3,842),pine)
    polygon(p,[(0,112),(595,112),(595,555),(0,776)],green)
    for j in range(13):
        x=-155+j*28
        p.draw_polyline([(0,136+j*7),(max(0,x+200),245+j*9),(max(0,x+184),369+j*8),(0,425+j*8)],color=(.16,.40,.25),width=.55)

def provincial(p,src,record):
    raw=' '.join(src.get_text().split());pat=r'Ce que disent les chiffres : (.+?) Position\. ([\d,]+) % de fonctions rouges sur ([\d ]+) évaluations calculables \((\d+) établissements, (\d+) zones\).*?part d.ensemble \(([\d,]+) %\).*?Fonctions vitales rouges dans (\d+) cas sur (\d+) \(([\d,]+) %\)';a=re.search(pat,raw);assert a,src.number
    province,pct,evals,fac,zones,overall,vital,base,vpct=a.groups();end=max(b[3] for b in src.get_text('blocks') if b[1]<785 and b[4].strip());y=end+14;h=min(202,p.rect.height-39-y);assert h>45
    # The compact layout uses the SAME two indicators when the page also has tables.
    large=h>=132;X=57;W=482;rect(p,(X,y,X+W,y+h),paper);rect(p,(X,y,X+4,y+h),green)
    text(p,69,y+(20 if large else 14),province,15 if large else 11,green,True)
    for j,(label,v) in enumerate([('fonctions rouges',pct),('Fonctions vitales rouges',vpct)]):
        x=69+j*236;w=211;vnum=float(v.replace(',','.'));yy=y+(53 if large else 29);text(p,x,yy,label,11 if large else 8,ink)
        if large:
            text(p,x,yy+45,v+' %',38,brick);bar=yy+60
        else:text(p,x+w,yy,v+' %',12,brick,True,align='right');bar=yy+7
        rect(p,(x,bar,x+w,bar+5),(.84,.88,.84));rect(p,(x,bar,x+w*vnum/100,bar+5),brick)
    if large:
        Y=y+h-27;line(p,69,Y-11,526,Y-11,mint);text(p,69,Y+5,evals+' évaluations calculables',11,green);text(p,299,Y+5,fac+' établissements, '+zones+' zones',11,green)
    record.append({'page':src.number+1,'type':'profil','zone':[X-1,y-1,X+W+1,y+h+1],'province':province,'valeurs':[pct,vpct],'evaluation':evals,'etablissements':fac,'zones':zones})

def section_name(n):
    # Real section titles, kept short for the running foot; no new editorial copy.
    options=[(2,'Préface'),(3,'Remerciements'),(4,'Table des matières'),(6,'Liste des figures et tableaux'),(9,'Abréviations et acronymes'),(11,'Résumé exécutif'),(14,'Introduction'),(17,'Approche méthodologique'),(26,'Résultats'),(83,'Discussion'),(89,'Conclusion et recommandations'),(96,'Bibliographie'),(100,'Annexes')]
    return next(label for start,label in reversed(options) if n>=start)

def finish_design():
    records=[];profiles=[100,105,110,115,119,124,129,134];openings={2,3,9,11,14,17,26,83,89,96,100}
    for idx,p in enumerate(D):
        n=idx+1;w,h=p.rect.width,p.rect.height
        if n==1:continue
        # No running footer or side rail: all navigation is in the masthead.
        title=section_name(n);text(p,w-57,23,title,8.5,green,align='right');records.append({'page':n,'type':'navigation','zone':[330,9,w-48,28],'titre':title})
        if n==83:
            text(p,56,37,str(n),8,green);records.append({'page':n,'type':'folio','zone':[55,28,72,43],'titre':str(n)})
        if n in [23,55,64]:records.append(graphic_supplement(p,n))
        if n in profiles:provincial(p,S[idx],records)
    (OUT/'zones_design.json').write_text(json.dumps(records,ensure_ascii=False,indent=1)+'\n')
