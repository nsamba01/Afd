"""Listes de navigation et graphiques de lecture ciblés, dans le gabarit Md_ref."""
from index_listes import lire_listes

def composer_listes():
    data=list(lire_listes(S));assert len(data)==122 and all(r[-1] for r in data)
    for n in [6,7,8]:
        p=D[n-1];rows=[r for r in data if r[0]==n]
        for link in p.get_links():p.delete_link(link)
        for ref in p.get_contents():D.update_stream(ref,b'')
        text(p,57,37,str(n),9,green,True);text(p,79,37,'ICHESS, LLC',9,green,True);text(p,142,37,'International Center for Health Systems Strengthening',8,ink);line(p,57,46,539,46,(.84,.88,.84))
        title={6:'Liste des figures et tableaux',7:'Liste des tableaux',8:'Tableaux des annexes'}[n]
        text(p,56,93,title,36,green);line(p,57,108,539,108,(.86,.88,.84));line(p,57,108,102,108,ochre,2)
        # Reference contents convention: folio at left, aligned entry with a fine vertical rule.
        start=120;end=802;split=[];section=None
        for _,kind,num,label,dest in rows:
            name='Liste des figures' if kind=='Figure' else 'Tableaux des annexes' if num.startswith('A') else 'Liste des tableaux'
            header=name if name!=section and name!=title else None;section=name
            lines=[''];size=10.3
            for word in label.split():
                v=(lines[-1]+' '+word).strip()
                if lines[-1] and sum(extent(c,size) for c in v)>379:lines.append(word)
                else:lines[-1]=v
            split.append((header,kind,num,lines,dest))
        heads=sum(bool(row[0]) for row in split);extra=sum(len(row[3])-1 for row in split);rowh=(end-start-heads*23-extra*11.1)/len(rows);assert rowh>=11,(n,rowh)
        y=start;line(p,87,start,87,end,(.82,.86,.82),.55)
        for header,kind,num,lines,dest in split:
            if header:
                rect(p,(93,y,539,y+19),paper);text(p,100,y+14,header,13,green,True);y+=23
            yy=y+rowh*.70
            text(p,78,yy,str(dest),10,green,True,align='right');text(p,95,yy,kind+' '+num+':',9.6,green);xx=157
            for j,lbl in enumerate(lines):text(p,xx,yy+j*11.1,lbl,size,ink,width=min(381,sum(extent(c,size) for c in lbl)))
            bottom=y+rowh+11.1*(len(lines)-1);line(p,94,bottom-.6,539,bottom-.6,(.91,.92,.90),.28)
            p.insert_link({'kind':m.LINK_GOTO,'from':m.Rect(55,y,539,bottom-.6),'page':dest-1,'to':m.Point(0,0)});y=bottom

def graphic_supplement(p,n):
    # Verbatim labels and figures; two different measures are never pooled.
    red=(.69,.22,.23);blue=(.14,.36,.48);gold=(.80,.64,.26);rows=[]
    def add(x,y,txt,size=10,col=ink,b=False,**kw):text(p,x,y,txt,size,col,b,**kw);rows.append(txt)
    if n==23:
        y=564;rect(p,(57,y,539,800),paper);rect(p,(57,y,61,800),green);add(70,586,'Rôle des douze dimensions dans les 71 spécifications',16,green,True)
        matrix=[('Organisation du service',68,3,0),("Capacité d'accueil",8,34,21),('Ressources humaines',57,14,0),('Intrants et produits',47,15,3),('Équipements',56,15,0),('Eau, hygiène et assainissement',0,54,9),('Électricité',8,40,23),('Communication',18,7,46),('Référence',20,33,13),('Données sanitaires',3,16,52),('Surveillance épidémiologique',5,5,61),('Intégration des services',5,18,46)]
        for j,(lbl,c) in enumerate(zip(['Bloquante','Restrictive','Contextuelle'],[red,gold,blue])):
            x=70+j*149;rect(p,(x,598,x+10,605),c);add(x+15,605,lbl,9)
        for k in [0,1]:
            for tick in [0,35,71]:
                xx=70+k*231+130*tick/71;line(p,xx,616,xx,784,mint,.5);add(xx,796,str(tick),7,green,align='center')
        for j,(label,*vals) in enumerate(matrix):
            x=70+j//6*231;Y=628+(j%6)*29;add(x,Y,label,9.3);xx=x
            for v,c in zip(vals,[red,gold,blue]):
                if v:rect(p,(xx,Y+4,xx+130*v/71,Y+9),c);xx+=130*v/71
            add(x+137,Y+10,' / '.join(map(str,vals)),8,green)
    elif n==55:
        y=285;rect(p,(57,y,539,656),paper);rect(p,(57,y,61,656),green)
        groups=[('indisponibilité le jour de la visite',[('ATPE','86,1'),('kit d’accouchement','78,1'),('kit anti-choc','78,1')]),('Les ruptures prolongées',[('artésunate-amodiaquine','33,1'),('artésunate en suppositoire','14,9'),('tests rapides VIH','13,0'),('artéméther-luméfantrine','11,9')])]
        for j,(title,items) in enumerate(groups):
            Y=316+j*171;add(72,Y,title,17,green,True)
            for tick in [0,25,50,75,100]:
                tx=251+212*tick/100;line(p,tx,Y+20,tx,Y+34+(len(items)-1)*29,mint,.6);add(tx,Y+47+(len(items)-1)*29,str(tick)+' %',8,green,align='center')
            for k,(label,v) in enumerate(items):
                yy=Y+32+k*29;add(73,yy,label,11);xx=251;w=212;rect(p,(xx,yy-7,xx+w,yy),mint);rect(p,(xx,yy-7,xx+w*float(v.replace(',','.'))/100,yy),red if j==0 else blue);add(520,yy,v+' %',12,green,True,align='right')
    elif n==64:
        y=604;rect(p,(57,y,539,801),paper);rect(p,(57,y,61,801),green);add(72,627,'Événements récents déclarés',17,green,True)
        items=[('rupture de médicaments essentiels','54,4'),('ruptures d’approvisionnement en eau','31,4'),('pannes prolongées d’électricité','23,9'),('épidémies ou flambées de maladie','15,6'),('absence prolongée de personnel clé','12,7'),('incidents sécuritaires','12,5'),('tempêtes ou événements climatiques majeurs','1,9')]
        for tick in [0,25,50,75,100]:
            tx=287+174*tick/100;line(p,tx,637,tx,785,mint,.6);add(tx,797,str(tick)+' %',8,green,align='center')
        for j,(label,v) in enumerate(items):
            Y=651+j*22;add(72,Y,label,10);xx=287;w=174;rect(p,(xx,Y-7,xx+w,Y),mint);rect(p,(xx,Y-7,xx+w*float(v.replace(',','.'))/100,Y),blue);add(521,Y,v+' %',11,green,True,align='right')
    return {'page':n,'type':'lecture','zone':[56,y-1,540,802 if n!=55 else 657],'libelles':rows}
