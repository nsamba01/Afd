# Les valeurs sont transcrites des étiquettes imprimées, sans mesurer les pixels.
provs='HK HL KC KO LM LL SK TG'.split();blue=(.13,.40,.61);navy=(.06,.20,.34);red=(.73,.20,.22)
def figure(n):
 p=D[n-1];im=p.get_images()[0];name=im[7].encode()
 for x in p.get_contents():
  data=D.xref_stream(x)
  if b'/'+name+b' Do' in data:D.update_stream(x,data.replace(b'/'+name+b' Do',b''))
 return p,m.Rect(S[n-1].get_image_info()[0]['bbox'])
p,box=figure(27);series=[[35,4,13],[7,2,3],[16,2,6],[4,2,2],[9,3,4],[13,7,4],[12,0,4],[5,2,1]];assert list(map(sum,zip(*series)))==[101,22,37]
for j,(label,c) in enumerate(zip(['Centres de santé (niveau 1)','Centres de santé de référence (niveau 1+)','Hôpitaux généraux de référence (niveau 2)'],[blue,green,navy])):
 y=78+j*13;rect(p,(284,y-7,296,y),c);text(p,302,y,label,9)
text(p,67,84,'établissements',9,ink)
for k in range(0,51,10):
 y=388-k*5.3;line(p,95,y,531,y,(.86,.89,.87));text(p,90,y+3,str(k),8,align='right')
for j,(name,vals) in enumerate(zip(provs,series)):
 x=105+54*j;y=388
 for v,c in zip(vals,[blue,green,navy]):
  if v:rect(p,(x,y-v*5.3,x+34,y),c);text(p,x+17,y-v*2.65+2,str(v),min(8,v*4),white,align='center');y-=v*5.3
 text(p,x+17,y-4,str(sum(vals)),9,navy,True,align='center');text(p,x+17,404,name,10,align='center')
p,box=figure(61);y=box.y0;text(p,60,y+10,"Centres de santé : la part de fonctions vitales rouges selon la présence déclarée d'une catégorie de personnel",9,green,True,width=471)
text(p,60,y+26,'% de fonctions vitales rouges',8);base=box.y1-19;scale=1.27
for j,(label,c) in enumerate(zip(['Aucun agent','Au moins un agent'],[red,blue])):
 x=337+j*90;rect(p,(x,y+19,x+9,y+26),c);text(p,x+13,y+26,label,8)
for k in range(0,101,20):
 Y=base-k*scale;line(p,81,Y,531,Y,(.86,.89,.87));text(p,77,Y+2,str(k),7,align='right')
for j,(cat,vals) in enumerate(zip(['Médecin généraliste','Sage-femme','Infirmier(ère)','Technicien de laboratoire'],[[(86,71),(81,30)],[(87,54),(81,47)],[(91,1),(84,100)],[(88,57),(79,44)]])):
 x=99+j*112
 for k,(v,n) in enumerate(vals):
  X=x+34*k;Y=base-v*scale;rect(p,(X,Y,X+33,base),[red,blue][k]);text(p,X+16,Y-11,str(v),9,ink,True,align='center');text(p,X+16,Y-2,f'(n={n})',7,ink,align='center')
 text(p,x+34,base+13,cat,8,ink,align='center')

def heat(n,title,unit,rows,values,maximum,c,totals=None):
 p,B=figure(n);y=B.y0;text(p,B.x0,y+9,title,9,green,True,width=B.width-4);text(p,B.x0,y+21,unit,8);top=y+29;bottom=B.y1-(28 if totals else 19);h=(bottom-top)/len(rows);cw=38;X=B.x1-9*cw;step=5 if maximum==35 else 10
 # Continuous scale with the original tick values.
 for k in range(maximum+1):
  t=k/maximum;C=tuple(.98+(a-.98)*t for a in c);rect(p,(B.x1-127+3*k*35/maximum,y+13,B.x1-127+3*(k+1)*35/maximum,y+16),C)
 for k in range(0,maximum+1,step):text(p,B.x1-127+105*k/maximum,y+23,str(k),5.5,align='center')
 for j,(label,row) in enumerate(zip(rows,values)):
  Y=top+j*h;text(p,X-6,Y+h*.67,label,8,align='right')
  for k,v in enumerate(row):
   xx=X+k*cw;t=v/maximum;C=tuple(.98+(a-.98)*t for a in c);rect(p,(xx,Y,xx+cw-.4,Y+h-.4),C);bold=bool(totals and ((j==2 and k!=7) or (j==3 and k==0) or (j==6 and k==7)));text(p,xx+cw/2,Y+h*.68,str(v),9,white if t>.58 else ink,bold,align='center')
 line(p,X+8*cw,top,X+8*cw,bottom,navy)
 for k,label in enumerate(provs+['Ensemble']):
  xx=X+(k+.5)*cw;text(p,xx,bottom+10,label,8,align='center');
  if totals:text(p,xx,bottom+20,str(totals[k])+(' rouges' if k<8 else ''),7,align='center')
heat(68,'Profil de blocage par province : part des fonctions rouges bloquées par chaque dimension','% des fonctions rouges de la province bloquées par la dimension',['Équipements','Intrants et produits','Référence','Organisation du service','Ressources humaines','Communication','Électricité','Intégration des services','Données sanitaires','Surveillance épidémiologique'],[[58,61,45,33,44,41,72,48,53],[51,58,48,50,56,46,67,42,53],[40,35,37,17,42,40,47,56,40],[25,18,10,4,20,33,31,14,23],[17,14,1,23,13,24,12,7,14],[4,3,15,0,11,9,16,11,8],[7,7,9,2,8,6,8,7,7],[4,1,0,0,4,6,3,0,3],[2,4,2,0,2,2,2,0,2],[3,0,1,0,1,1,2,0,2]],72,red)
heat(81,'Où chaque levier pèse le plus : gain simulé par province (gras : premier levier de la province)','% des fonctions rouges de la province libérées',['Organisation du service','Ressources humaines','Intrants et produits','Équipements','Électricité','Communication','Référence','Intégration des services'],[[0,0,1,0,1,1,0,0,0],[1,0,0,11,1,2,0,0,1],[11,15,18,35,15,10,8,11,13],[11,13,11,18,7,10,5,11,10],[2,2,2,2,2,2,0,7,2],[1,1,6,0,3,2,1,1,2],[6,2,10,7,6,7,0,15,6],[2,0,0,0,2,4,2,0,2]],35,navy,[901,224,353,82,285,323,322,89,2579])
yellow=(.94,.71,.08);tones=[(.91,.63,.61),(.83,.38,.36),red,(.43,.10,.12)]
def legend(p,x,y,labels,colors,dx):
 for j,(lbl,c) in enumerate(zip(labels,colors)):
  xx=x+j*dx;rect(p,(xx,y-6,xx+8,y),c);text(p,xx+11,y,lbl,7)
def ticks(p,X,Y,w,tickvals,maxval):
 for k in tickvals:text(p,X+w*k/maxval,Y,str(k),7,ink,align='center')
def stack(p,X,Y,w,h,vals,labels,cols,den=100):
 for v,lbl,c in zip(vals,labels,cols):
  ww=w*v/den
  if ww:rect(p,(X,Y,X+ww,Y+h),c)
  if lbl:text(p,X+ww/2,Y+h*.5+2.2,str(lbl),min(8,h*.83),ink if c in (yellow,tones[0]) else white,align='center')
  X+=ww
# Figure 2 : associer les proportions du tableau 7 à l’ordre et aux arrondis de la figure.
rows=[]
for n in [30,31]:
 z=S[n-1].get_text().split('où rouge')[-1].split('Lecture du tableau')[0];matches=re.findall(r'(?:^|\n)(\d+)\s+([\wÀ-ÿ ’\'\-+.\n]+?)\s+(Vitale|Essentielle|Systémique)\s+(\d+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)',z)
 for _,name,crit,K,*v in matches:
  name=re.sub(r'^\d+ ', '', ' '.join(name.split())).replace('- ','-');v=[float(a.replace(',','.')) for a in v];rows.append((name,crit,int(K),v))
assert len(rows)==28
rows.sort(key=lambda row:-row[3][2]);p,B=figure(29);y=B.y0;text(p,B.x0,y+10,'Classification des fonctions traceuses — Ensemble des 160 établissements (★ fonction vitale)',10,green,True,width=B.width-4)
X=B.x0+111;W=(B.width-111-6)/1.2;top=y+22;H=(B.height-65)/28
for j,(cat,crit,K,vals) in enumerate(rows):
 Y=top+j*H;text(p,X-4,Y+H*.64,cat+(' ★' if crit=='Vitale' else ''),7.8,align='right');stack(p,X,Y,W,H*.77,vals,[str(round(v)) if v>=7.5 else '' for v in vals],[green,yellow,red],sum(vals));text(p,X+W+4,Y+H*.64,'K = '+str(K),7)
ticks(p,X,B.y1-29,W*1.2,range(0,121,20),120);text(p,B.x0+B.width/2,B.y1-18,'% des évaluations calculables (Vert + Jaune + Rouge = 100)',8,align='center');legend(p,B.x0+38,B.y1-4,['Vert — opérationnelle','Jaune — réalisable, instable','Rouge — non réalisable'],[green,yellow,red],140)
# Figure 13 : effectifs exacts du tableau A58, libellés arrondis tels qu'imprimés.
p,B=figure(52);text(p,B.x0,B.y0+10,'Profondeur du blocage : nombre de dimensions bloquantes par fonction rouge',10,green,True);X=B.x0+95;W=B.width-100;H=(B.height-55)/4
for j,(cat,vals,labs) in enumerate(zip(['Ensemble (2579 rouges)','Niveau 1 (CS)','Niveau 1+ (CSR)','Niveau 2 (HGR)'],[[939,856,555,229],[523,654,449,194],[164,98,59,17],[252,104,47,18]],[[36,33,22,9],[29,36,25,11],[48,29,18,''],[60,25,11,'']])):
 Y=B.y0+17+j*H;text(p,X-5,Y+H*.47,cat,8,align='right');stack(p,X,Y,W,H*.7,vals,labs,tones,sum(vals))
ticks(p,X,B.y1-25,W,range(0,101,20),100);text(p,X+W/2,B.y1-15,'% des fonctions rouges',8,align='center');legend(p,B.x0+65,B.y1-3,['1 blocage','2 blocages','3 blocages','4 blocages ou plus'],tones,92)
# Figure 14 : configurations exactes et effectifs imprimés.
p,B=figure(53);text(p,B.x0,B.y0+10,'Les douze configurations de blocage les plus fréquentes',11,green,True);X=B.x0+142;top=B.y0+22;W=B.width-179;H=(B.height-59)/12
for j,(lbl,v,k) in enumerate(zip(['Intrants','Équipements','Intrants + Équipements','Intrants + Équipements + Référence','Équipements + Référence','Référence','Intrants + Référence','Équipements + Électricité','Données sanitaires','Électricité','Communication','Intégration des services'],[13.1,10.2,10.1,8.5,7.7,6.5,6.0,2.4,2.1,2.1,1.9,1.8],[338,262,261,219,199,167,154,61,53,53,50,46])):
 Y=top+j*H;text(p,X-4,Y+H*.58,lbl,7.35,align='right');xx=X+W*k/2579*100/16;rect(p,(X,Y,xx,Y+H*.73),tones[lbl.count('+')]);text(p,xx+3,Y+H*.58,str(v).replace('.',',')+f' %  (n = {k})',7.5)
ticks(p,X,B.y1-27,W,range(0,17,2),16);text(p,X+W/2,B.y1-17,'% des 2 579 fonctions rouges',8,align='center');text(p,B.x0,B.y1-3,'Nombre de dimensions',7.5);legend(p,B.x0+88,B.y1-3,['1 dimension','2','3','4 ou plus'],tones,83)
# Figure 20 : effectifs exacts du tableau A62 (les sept étapes présentées dans la figure).
p,B=figure(77);text(p,B.x0,B.y0+10,'Paquets cumulatifs de leviers : fonctions rouges libérées à mesure que les dimensions sont résolues',10,green,True,width=B.width-4);legend(p,B.x0+5,B.y0+24,['rouge → vert','rouge → jaune'],[green,yellow],75);text(p,B.x1,B.y0+24,'fonctions rouges libérées (cumul)',8,align='right');base=B.y1-15;scale=(B.height-70)/2579;X=B.x0+28;W=B.width-34
for k in range(0,2501,500):
 Y=base-scale*k;line(p,X,Y,B.x1,Y,(.86,.89,.87));text(p,X-4,Y+2,str(k),7,align='right')
Y=base-scale*2579;line(p,X,Y,B.x1,Y,red);text(p,B.x1,Y-3,'2 579 fonctions rouges',7,red,align='right')
for j,(cat,a,b,pc) in enumerate(zip(['intrants','+ équipements','+ référence','+ eau-hygiène','+ électricité','+ RH','+ organisation'],[19,36,55,215,397,696,1363],[319,825,1545,1385,1372,1183,947],[13,33,62,62,69,73,90])):
 x=X+(j+.5)*W/7;half=W/19;Y=base
 for v,c in [(a,green),(b,yellow)]:rect(p,(x-half,Y-v*scale,x+half,Y),c);Y-=v*scale
 text(p,x,Y-3,f'{a+b} · {pc} %',7,navy,True,align='center');text(p,x,base+11,cat,7,align='center')
# Figure 4 : conserver les parenthèses imprimées pour les petits dénominateurs.
p,B=figure(35);x=B.x0;y=B.y0;text(p,x,y+10,'Part de fonctions rouges par fonction et par province',10,green,True);text(p,B.x1,y+10,'% de fonctions rouges',8,align='right');names="CPN de routine|CPN + PTME|Grossesse à risque|Accouchement normal|Hémorragie post-partum|Pré-éclampsie|Sepsis obstétrical|Accouchement assisté|Césarienne d'urgence|Transfusion|Réanimation néonat.|Soins du nouveau-né|CPoN mère|CPoN nouveau-né|Réception urgences|Diagnostic paludisme|Paludisme simple|Paludisme grave|Dépistage nutrition|MA non compliquée|MA compliquée|Vaccination de routine|Chaîne du froid|MAPI|Surveillance épidémio|Référence urgente|Intégration services|Données sanitaires".split('|');matrix='''90 100 94 33 100 55 100 57 83
74 67 61 17 75 75 92 43 69
97 100 100 67 100 70 100 86 92
100 100 96 75 88 88 100 50 92
73 92 71 62 62 54 100 38 71
81 100 83 75 94 67 100 62 82
77 75 58 38 81 54 100 38 69
88 100 62 (75) 57 64 (100) (0) 73
88 100 88 (100) 86 36 (100) (0) 76
76 100 75 (75) 71 64 (100) (67) 76
88 100 88 88 94 75 100 62 88
83 100 58 75 94 58 100 38 77
88 100 96 38 94 54 100 62 83
69 100 67 25 81 46 94 62 69
77 (100) 50 (50) (100) (25) (100) (100) 73
10 17 8 12 25 0 38 0 12
37 33 33 50 44 8 56 0 33
83 100 83 50 88 67 94 88 82
77 75 4 12 50 71 94 25 58
100 100 100 (100) 100 92 100 80 98
100 100 79 50 94 92 100 62 91
100 78 67 33 83 65 100 71 81
95 78 67 33 75 60 100 71 78
100 100 94 33 100 75 100 71 90
29 17 29 0 38 21 44 12 27
77 83 71 25 100 54 100 75 75
40 8 0 0 38 46 38 0 28
35 67 29 0 44 29 38 0 33'''.splitlines();X=x+112;cw=(B.x1-X)/9;H=(B.height-61)/28
for j,(name,row) in enumerate(zip(names,matrix)):
 Y=y+30+j*H;text(p,X-4,Y+H*.7,name,7.5,align='right')
 for k,lbl in enumerate(row.split()):
  v=int(lbl.strip('()'))/100;xx=X+k*cw;rect(p,(xx,Y,xx+cw-.3,Y+H-.3),tuple(.98+(c-.98)*v for c in red));text(p,xx+cw/2,Y+H*.7,lbl,8,white if v>.6 else ink,align='center')
for j,(cat,num) in enumerate(zip(provs+['Ensemble'],[52,12,24,8,16,24,16,8,160])):
 xx=X+(j+.5)*cw;text(p,xx,B.y1-18,cat,8,align='center');text(p,xx,B.y1-7,f'{num} ét.',7,align='center')
for j,v in enumerate(range(0,101,20)):
 xx=x+80+j*54;rect(p,(xx,y+15,xx+11,y+22),tuple(.98+(c-.98)*v/100 for c in red));text(p,xx+14,y+22,str(v),7)
# Figure 8 : le dénominateur et les arrondis donnent ici une solution entière unique.
def counts(K,labs):
 import itertools
 opts=[[n for n in range(K+1) if l is None or round(100*n/K)==l] for l in labs];sol=[v for v in itertools.product(*opts) if sum(v)==K];assert len(sol)==1,(K,labs);return sol[0]
p,B=figure(43);legend(p,B.x0,B.y0+9,['tous les couples documentés','une partie (occasion manquée)','aucun'],[green,yellow,red],160);top=B.y0+19;H=(B.height-52)/12;X=B.x0+111;W=(B.width-116)/1.2
for j,(cat,K,labels) in enumerate(zip(['Niveau 1 (CS)','Niveau 1+ (CSR)','Niveau 2 (HGR)'],[101,22,37],[[[46,31,24],[52,44,None],None],[[73,23,None],[73,18,9],[59,23,18]],[[84,14,None],[70,30,None],[57,30,14]]])):
 Y=top+4*j*H;text(p,B.x0,Y+H*.72,cat,9,green,True)
 for k,(title,labs) in enumerate(zip(['Contacts maternels',"Consultations de l'enfant",'Intégration de la référence'],labels)):
  yy=Y+(k+1)*H;text(p,X-4,yy+H*.6,title,8,align='right');text(p,X+W+4,yy+H*.6,'K = '+str(K if labs else 0),7)
  if labs:stack(p,X,yy,W,H*.75,counts(K,labs),labs,[green,yellow,red],K)
  else:text(p,X+3,yy+H*.6,'non mesurée au niveau 1',8)
ticks(p,X,B.y1-16,W*1.2,range(0,121,20),120);text(p,X+W/2,B.y1-4,'% des établissements',8,align='center')
# Figure 11 : les étiquettes sont des pourcentages publiés, pas des effectifs.
p,B=figure(49);cw=B.width/4;top=B.y0+6
for j,(title,vals) in enumerate(zip(['Reconnaissance du signal','Rapidité de la notification','Outils et transmission','Analyse et décision'],[[78,12,10],[90,5,5],[30,39,31],[68,19,14]])):
 xx=B.x0+j*cw;rect(p,(xx,top,xx+cw-7,B.y1-26),(.95,.97,.95));wrap(p,title,xx+6,top+18,cw-20,10,green);text(p,xx+6,top+49,'160 établissements',8);stack(p,xx+5,top+61,cw-18,17,vals,[f'{v} %' if v>=18 else '' for v in vals],[green,yellow,red],sum(vals));text(p,xx+5,top+93,f'vert {vals[0]} · jaune {vals[1]} · rouge {vals[2]}',7);text(p,xx+5,top+106,f'point de rupture : {vals[2]} %',8,red,True)
 if j<3:text(p,xx+cw-6,top+70,'→',8,navy)
wrap(p,'Vert : complet et régulier · Jaune : partiel ou irrégulier · Rouge : absent. Détection → notification (surveillance) ; outils et transmission → analyse et décision (données).',B.x0,B.y1-14,B.width,7,ink)
# Figure 15 : nombre de fonctions jaunes et sous-ensemble à fragilité unique.
p,B=figure(54);text(p,B.x0,B.y0+9,'Fonctions jaunes : combien sont à une seule fragilité du vert, et laquelle',10,green,True);X=B.x0+100;W=143;H=(B.height-59)/28;top=B.y0+24
cats="Diagnostic paludisme|Intégration services|Surveillance épidémio|Paludisme simple|Données sanitaires|Dépistage nutrition|CPoN nouveau-né|Hémorragie post-partum|Sepsis obstétrical|Référence urgente|CPN + PTME|Soins du nouveau-né|Paludisme grave|Chaîne du froid|Pré-éclampsie|CPoN mère|Vaccination de routine|CPN de routine|Réanimation néonat.|Accouchement assisté|MA compliquée|Césarienne d'urgence|Transfusion|MAPI|Accouchement normal|Réception urgences|Grossesse à risque|MA non compliquée".split('|');dom=['Référence','Données sanitaires','Électricité','Eau, hygiène et assainissement','Intrants et produits','Organisation du service','Ressources humaines',"Capacité d'accueil"]
for j,(lbl,K,v,idx) in enumerate(zip(cats,[134,110,109,102,95,61,50,47,46,40,37,36,29,27,27,27,23,20,19,16,14,14,12,12,11,10,10,2],[12,20,22,14,19,23,1,6,6,6,0,1,4,5,5,0,3,0,3,4,5,2,5,3,0,2,0,1],[0,0,1,0,2,0,3,4,3,4,5,4,4,5,3,5,5,5,4,3,3,6,3,5,0,7,5,3])):
 Y=top+j*H;text(p,X-12,Y+H*.68,lbl,7.2,align='right');stack(p,X,Y,W,H*.76,[v,K-v],['',''],[green,yellow],200)
 if v:text(p,X-3,Y+H*.68,str(v),6,green,True,align='right')
 text(p,X+W+5,Y+H*.68,f'{K} jaunes · dominante (toutes jaunes) : {dom[idx]}',6.1)
ticks(p,X,B.y1-24,W,[0,50,100,150,200],200);text(p,X+W/2,B.y1-15,'fonctions jaunes',7,align='center');legend(p,B.x0,B.y1-4,['fragilité unique (passe au vert si elle est levée)','deux fragilités ou plus'],[green,yellow],224)
# Figure 16 : deux effectifs indépendants par ligne (total en déficit et sorties du rouge).
p,B=figure(58);text(p,B.x0,B.y0+10,'Rétablir un seul élément libère peu de fonctions : les autres blocages subsistent',10,green,True);X=B.x0+186;W=B.width-225;H=(B.height-56)/20;top=B.y0+22
labels='Artésunate + amodiaquine (AS-AQ), comprimé — N1|Artéméther + luméfantrine (AL), comprimé — N1|Source de chaleur (salle et nouveau-né) — N1|Kit d’accouchement à usage unique — N1|Bandelettes urinaires (protéinurie) — N1|Seringues et aiguilles — N2|Source de chaleur (salle et nouveau-né) — N2|Artésunate + amodiaquine (AS-AQ), comprimé — N2|Artéméther + luméfantrine (AL), comprimé dispersible — N2|Source de chaleur (salle et nouveau-né) — N1+|ATPE (aliment thérapeutique prêt à l’emploi) — N1|Sulfate de magnésium — N1|Tests rapides VIH — N1|Échelle de coma (Glasgow / Blantyre) — N2|Kit d’accouchement à usage unique — N2|Artésunate, suppositoire — N1|Bandelettes urinaires (protéinurie) — N1+|Réfrigérateur à sang ou banque de sang — N1+|Forceps obstétricaux — N1+|Forceps obstétricaux — N2'.split('|')
for j,(cat,a,b) in enumerate(zip(labels,[33,33,30,15,15,15,14,11,11,10,9,8,8,8,8,8,7,7,7,7],[34,34,154,84,154,44,38,11,11,28,87,77,55,10,28,62,24,17,13,17])):
 Y=top+j*H;text(p,X-4,Y+H*.63,cat,6.7,width=min(181,fonts.get(choose(cat),backup[False]).text_length(cat,fontsize=6.7)),align='right');stack(p,X,Y,W,H*.73,[a,b-a],['',''],[blue,(.80,.87,.90)],160);text(p,X+W*b/160+3,Y+H*.63,f'{a} / {b}',7)
ticks(p,X,B.y1-25,W,range(0,161,20),160);text(p,X+W/2,B.y1-16,'Nombre de fonctions rouges (base de référence)',7.5,align='center');legend(p,B.x0,B.y1-4,['Fonctions rouges où l’élément est en déficit','Fonctions qui sortent du rouge si l’élément seul est rétabli'],[(.80,.87,.90),blue],220)
# Independent mini-bars for published rounded percentages. '+' = coloured segment without a
# printed value: a hollow mark, never a numerical estimate. '-' = no visible segment.
def mark(p,x,y,w,h,v,c,maxv=100):
 if v=='-':return
 if v=='+':p.draw_circle((x+w/2,y+h/2),min(2,h/4),color=c,width=.8);return
 val=float(v);rect(p,(x,y,x+w,y+h),(.96,.97,.96));rect(p,(x,y,x+w*val/maxv,y+h),tuple(.68+.32*a for a in c));text(p,x+w/2,y+h*.5+2,str(v),min(8,h*.93),ink,align='center')
def charthead(p,B,t):text(p,B.x0,B.y0+10,t,10,green,True,width=min(B.width,fonts.get(choose(t,True),backup[True]).text_length(t,fontsize=10)))
# Figure 3 : trois panneaux ; K commun à chaque ligne du panneau.
p,B=figure(34);charthead(p,B,'Préparation opérationnelle des 17 fonctions communes');text(p,B.x0,B.y0+22,'Comparaison des CS, CSR et HGR • Pourcentage par fonction et par niveau de soins',8);levels=['CS','CSR','HGR'];labels='Accouchement normal|Hémorragie du post-partum|Pré-éclampsie|Sepsis obstétrical|Réanimation néonatale|Soins du nouveau-né|Soins postnatals de la mère|Soins postnatals du nouveau-né|Diagnostic du paludisme|Paludisme simple|Paludisme grave|Dépistage nutritionnel|Malnutrition aiguë compliquée|Surveillance épidémiologique|Référence urgente|Intégration des services|Données sanitaires'.split('|');panels=['93 + +;85 15 -;93 + +;84 14 +;98 + +;85 14 +;90 10 -;82 18 -;6 91 +;36 61 +;95 + -;66 30 +;93 + -;28 68 +;79 21 -;32 66 +;39 57 +','91 9 -;45 55 -;68 32 -;41 59 -;77 23 -;68 32 -;73 27 -;64 36 -;23 73 +;27 73 -;82 18 -;59 41 -;91 9 -;23 73 +;64 36 -;18 77 +;14 77 9','92 8 -;46 54 -;62 38 -;46 51 +;65 32 +;59 41 -;70 30 -;35 65 -;24 70 +;30 65 +;46 54 -;35 59 +;84 14 +;27 65 8;70 30 -;24 70 +;30 54 16'];X=B.x0+118;W=(B.x1-X)/3;H=(B.height-95)/17;top=B.y0+55
for k,(level,K,panel) in enumerate(zip(levels,[101,22,37],panels)):
 xx=X+k*W;text(p,xx+W/2,B.y0+35,f'{level} · {K} établissements',8,green,True,align='center');
 for l,t in enumerate(['Rouge','Jaune','Vert','K']):text(p,xx+(l+.5)*W/4,B.y0+47,t,7,ink,align='center')
 for j,(cat,row) in enumerate(zip(labels,panel.split(';'))):
  Y=top+j*H
  if k==0:text(p,X-3,Y+H*.68,cat,7,align='right')
  for l,(v,c) in enumerate(zip(row.split(),[red,yellow,green])):mark(p,xx+l*W/4,Y,W/4-1,H*.78,v,c)
  text(p,xx+W*.875,Y+H*.68,str(K),7,align='center')
 ticks(p,xx+4,B.y1-27,W-12,[0,50,100],100)
text(p,B.x0,B.y1-15,'K : nombre d’établissements disposant d’une classification pour la fonction.',7);text(p,B.x0,B.y1-4,'Pourcentages arrondis à l’unité ; les petites proportions sont représentées sans étiquette.',7)
# Figure 5.
p,B=figure(36);charthead(p,B,'Profil par domaine technique');legend(p,B.x0,B.y0+24,['Vert — opérationnelle','Jaune — réalisable, instable','Rouge — non réalisable'],[green,yellow,red],155)
for j,(cat,raw) in enumerate(zip(['Ensemble','Niveau 1 (CS)','Niveau 1+ (CSR)','Niveau 2 (HGR)'],['+ 21 79 1863;+ 55 42 480;+ 18 80 421;- 17 83 369;+ 55 41 640','+ 11 88 1111;+ 52 46 303;+ 13 86 303;- 13 87 303;+ 53 44 404','- 33 67 308;+ 55 44 66;- 25 75 44;- 35 65 66;+ 66 30 88','+ 35 64 444;+ 63 33 111;+ 36 59 74;+ 55 38 148'])):
 xx=B.x0+(j%2)*241;yy=B.y0+40+(j//2)*130;text(p,xx,yy,cat,10,green,True);cats=['SMNEA','Paludisme','Nutrition','Vaccination','Transversal'] if j!=3 else ['SMNEA','Paludisme','Nutrition','Transversal'];
 for l,name in enumerate(['Vert','Jaune','Rouge','K']):text(p,xx+63+44*l,yy+14,name,7,align='center')
 for k,(name,row) in enumerate(zip(cats,raw.split(';'))):
  Y=yy+21+k*14;text(p,xx+42,Y+7,name,7.2,align='right');v=row.split();
  for l,c in enumerate([green,yellow,red]):mark(p,xx+45+l*44,Y,40,10,v[l],c)
  text(p,xx+197,Y+7,'K = '+v[-1],7,align='center')
 ticks(p,xx+48,yy+101,124,[0,25,50,75,100],100);text(p,xx+116,yy+113,'% des évaluations calculables',7,align='center')
# Figure 6 : certaines sommes imprimées dépassent 100 %. Ne pas les normaliser.
p,B=figure(37);charthead(p,B,'Fonctions vitales dont le service est déclaré offert : la majorité ne réunit pas les conditions à la visite');X=B.x0+228;cw=61;H=(B.height-52)/30
for j,title in enumerate(['Vert','Jaune','Rouge','n']):text(p,X+(j+.5)*cw,B.y0+23,title,7,ink,align='center')
labels=['Réanimation néonatale immédiate','Prise en charge du paludisme grave et de ses com','Détection, stabilisation initiale et orientation','Prise en charge de la pré-éclampsie/éclampsie','Prise en charge initiale et notification des MAP','Prise en charge de la malnutrition aiguë sévère',"Prévention et prise en charge de l’hémorragie du","Transfusion sanguine d'urgence",'Prise en charge du sepsis maternel ou puerpéral','Maintien et surveillance de la chaîne du froid','Accouchement vaginal assisté',"Césarienne d'urgence"]
raw='0 N1 - + 99 98;1 N1 - + 95 99;2 N1 - + 95 97;3 N1 + + 94 98;4 N1 - 8 93 96;5 N1 - 16 89 44;6 N1 - 15 87 97;7 N1+ - 14 86 22;1 N1+ - 19 86 21;8 N1 + 14 86 97;9 N1 - 18 83 96;4 N1+ - 22 83 18;5 N1+ - 17 83 12;10 N1+ - 18 82 22;11 N2 - 19 81 37;2 N1+ - 24 81 21;0 N1+ - 23 77 22;5 N2 + 19 77 26;7 N2 + 24 70 37;3 N1+ - 32 68 22;11 N1+ - 32 68 22;10 N2 - 32 68 37;0 N2 + 32 65 37;3 N2 - 38 62 37;9 N1+ - 56 50 18;6 N2 - 54 46 37;8 N2 + 51 46 37;1 N2 - 54 46 37;6 N1+ - 55 45 22;8 N1+ - 59 41 22'
for j,row in enumerate(raw.split(';')):
 idx,level,g,a,r,n=row.split();Y=B.y0+28+j*H;text(p,X-4,Y+H*.73,labels[int(idx)]+' — '+level,6.7,align='right');
 for k,(v,c) in enumerate(zip([g,a,r],[green,yellow,red])):mark(p,X+k*cw,Y,cw-3,H*.9,v,c)
 text(p,X+3.5*cw,Y+H*.73,'n = '+n,6.7,align='center')
ticks(p,X,B.y1-13,cw*3,range(0,101,20),100);text(p,B.x0+B.width/2,B.y1-3,'% des fonctions dont le service est déclaré offert (état observé à la visite)',7,align='center')
# Figure 7.
p,B=figure(38);text(p,B.x0,B.y0+10,"Fonctions d'urgence : classification",9,green,True);text(p,B.x0+243,B.y0+9,"Au moins une fonction d’urgence rouge",9,green,True);text(p,B.x0+243,B.y0+20,"pour absence d’un élément critique d’urgence",9,green,True);X=B.x0+75;H=(B.height-69)/12;W=35
for j,(cat,raw,pc,a,b) in enumerate(zip(['Ensemble','Niveau 1 (CS)','Niveau 1+ (CSR)','Niveau 2 (HGR)','Haut-Katanga','Haut-Lomami','Kasaï-Central','Kasaï-Oriental','Lomami','Lualaba','Sankuru','Tanganyika'],['+ 19 81 1580','+ 9 90 909','- 28 72 264','+ 34 65 407','+ 14 85 506','- + 95 120','+ 20 79 234','+ 39 58 82','- 12 88 161','- 35 65 245','- + 99 152','- 40 60 80'],[72,83,59,49,67,83,62,62,94,62,100,50],[115,84,13,18,35,10,15,5,15,15,16,4],[160,101,22,37,52,12,24,8,16,24,16,8])):
 Y=B.y0+32+j*H;v=raw.split();text(p,X-4,Y+H*.62,cat,7.5,align='right')
 for l,c in enumerate([green,yellow,red]):mark(p,X+l*W,Y,W-2,H*.76,v[l],c)
 text(p,X+3*W+2,Y+H*.62,'K = '+v[3],7);xx=B.x0+248;ww=143*a/b;rect(p,(xx,Y,xx+ww,Y+H*.76),red);text(p,xx+ww+3,Y+H*.62,f'{pc} %  ({a} / {b})',7)
ticks(p,X,B.y1-26,120,range(0,121,20),120);ticks(p,B.x0+248,B.y1-26,179,range(0,126,25),125);text(p,X,B.y1-16,"% des fonctions d'urgence calculables",7);text(p,B.x0+290,B.y1-16,"% d’établissements",7);legend(p,B.x0,B.y1-3,['Vert — opérationnelle','Jaune — réalisable, instable','Rouge — non réalisable'],[green,yellow,red],157)
# Figure 9 : ne pas répartir le résidu d'arrondi entre les jours non étiquetés.
p,B=figure(44);X=B.x0+164;cw=50;H=(B.height-76)/21;cols=[red,(.86,.43,.13),yellow,(.47,.68,.40),green];series=['0 j','1–7 j','8–30 j','31–89 j','90–92 j'];
for k,lbl in enumerate(series):text(p,X+(k+.5)*cw,B.y0+12,lbl,8,align='center')
rows='''N1|CPN|s|+ + 80 11 +|101
N1|CPN|p|14 13 44 10 20|101
N1|Maternité|p|+ 49 + + 41|101
N1|CPoN|s|+ + 59 + 26|101
N1|CPoN|p|+ 16 44 + 30|101
N1|Paludisme|p|+ 22 + + 64|101
N1|Nutrition|p|56 + + + 32|98
N1|Vaccination|s|+ + 58 27 9|101
N1+|CPN|s|+ + 73 14 +|22
N1+|CPN|p|+ 27 45 + 18|22
N1+|Maternité|p|9 32 + 9 45|22
N1+|CPoN|s|- + 64 + 27|22
N1+|CPoN|p|+ 27 18 - 50|22
N1+|Paludisme|p|+ 27 9 + 55|22
N1+|Nutrition|p|55 14 + - 27|22
N1+|Vaccination|s|14 - 59 23 +|22
N2|Maternité|p|+ 14 + 8 68|37
N2|CPoN|s|- + 51 14 30|37
N2|CPoN|p|+ 24 27 16 30|37
N2|Paludisme|p|- 16 + + 76|37
N2|Nutrition|p|27 11 - + 57|37'''.replace('p|+ 14 + 8 68','p|8 14 + 8 68').splitlines()
for j,row in enumerate(rows):
 level,cat,mode,vs,n=row.split('|');Y=B.y0+22+j*H;text(p,X-4,Y+H*.65,level+' · '+cat+' · '+('Jours de service assurés' if mode=='s' else 'Jours de présence'),7,align='right')
 for k,(v,c) in enumerate(zip(vs.split(),cols)):mark(p,X+k*cw,Y,cw-3,H*.78,v,c)
 text(p,X+5*cw+3,Y+H*.65,'n = '+n,7)
ticks(p,X,B.y1-36,cw*5,range(0,101,20),100);text(p,B.x0,B.y1-24,'% des établissements renseignés — jours déclarés sur les trois derniers mois (valeurs valides 0–92)',8);legend(p,B.x0,B.y1-9,series[:-1]+['90–92 j (toute la période)'],cols,89)
# Figure 10 : six catégories distinctes, non agrégées.
p,B=figure(48);charthead(p,B,"Parcours : lorsque l'amont est classé vert ou jaune (presque toujours jaune), l'aval vital est rouge dans une large part des cas");X=B.x0+176;cw=33;H=(B.height-65)/16;cols=[green,yellow,red,(.40,.67,.45),(.94,.79,.43),(.84,.47,.47)];cats="Consultation prénatale → détection et orientation des grossesses à ris|Consultation prénatale → CPN intégrée à la PTME|Accouchement normal → prise en charge de l’hémorragie du post-partum|Accouchement normal → prise en charge de la pré-éclampsie|Accouchement normal → réanimation néonatale immédiate|Accouchement normal → soins essentiels du nouveau-né|Accouchement normal → consultation postnatale de la mère|Diagnostic du paludisme → traitement du paludisme simple|Traitement simple → stabilisation pré-référence du paludisme grave|Dépistage nutritionnel → malnutrition aiguë compliquée|Dépistage nutritionnel → malnutrition aiguë non compliquée (CS)|Vaccination de routine → chaîne du froid|Vaccination de routine → prise en charge des MAPI|Hémorragie du post-partum → référence et contre-référence urgente|Hémorragie du post-partum → transfusion (CSR, HGR)|Accouchement assisté → césarienne d’urgence (CSR, HGR)".split('|');raw='- - + - 43 52;+ - - - 71 24;- 8 - - 67 25;- 8 - - 58 33;- - 8 - 42 50;- - 8 - 42 50;- 8 - - 42 50;+ - + - 69 26;- + + - 21 74;+ + + - 16 75;- - 12 - + 82;- - - - 91 9;- - - - 30 70;- - - - 60 40;- - - 6 28 66;- - - - 50 50';
for k,title in enumerate(['vert → vert','vert → jaune','vert → rouge','jaune → vert','jaune → jaune','jaune → rouge']):text(p,X+(k+.5)*cw,B.y0+23,title,5.5,align='center')
for j,(cat,row,n,am) in enumerate(zip(cats,raw.split(';'),[21,21,12,12,12,12,12,140,107,67,34,23,23,47,32,16],[1,1,1,1,1,1,1,6,5,6,4,0,0,0,0,0])):
 Y=B.y0+29+j*H;f=fonts.get(choose(cat),backup[False]);text(p,X-3,Y+H*.7,cat,6.2,width=min(172,f.text_length(cat,fontsize=6.2)),align='right');
 for k,(v,c) in enumerate(zip(row.split(),cols)):mark(p,X+k*cw,Y,cw-1,H*.85,v,c)
 text(p,X+6*cw+2,Y+H*.7,f'n = {n} (dont {am} amont vert)',6)
ticks(p,X,B.y1-23,6*cw,[0,20,40,60,80,100,120],120);text(p,B.x0,B.y1-14,"% des établissements dont l'amont est classé vert ou jaune — état de l'aval dans le même établissement (trois couleurs conservées)",7);legend(p,B.x0,B.y1-3,['amont vert → aval vert','amont vert → aval jaune','amont vert → aval rouge','amont jaune → aval vert','amont jaune → aval jaune','amont jaune → aval rouge'],cols,78)
# Figure 12 : sous-série « premier blocage » du tableau 18 ; les valeurs non
# disponibles pour les quatre dimensions supplémentaires ne sont pas estimées.
p,B=figure(51);X=B.x0+113;W=148;H=(B.height-54)/12;text(p,X,B.y0+10,'Dimensions bloquantes (fonctions rouges)',8,green,True);text(p,X+W+34,B.y0+10,'Fragilités (fonctions jaunes)',8,green,True);cats=['Équipements','Intrants et produits','Référence','Organisation du service','Ressources humaines','Communication','Électricité','Intégration des services','Données sanitaires','Surveillance épidémiologique',"Capacité d'accueil",'Eau, hygiène et assainissement'];
for j,(cat,n,lab,prem,flab) in enumerate(zip(cats,[1370,1357,1038,583,369,219,188,81,53,38,2,0],[53,53,40,23,14,8,7,3,2,2,0,0],[451,1101,153,583,122,68,53,None,None,None,None,0],[23,30,51,27,44,10,33,3,25,3,18,44])):
 Y=B.y0+19+j*H;text(p,X-4,Y+H*.66,cat,7,align='right');ww=W*n/2579/.6
 if n:rect(p,(X,Y,X+ww,Y+H*.8),red)
 if prem:rect(p,(X,Y+H*.22,X+W*prem/2579/.6,Y+H*.60),tones[3])
 if prem is None and j in [7,8]:p.draw_circle((X+2,Y+H*.43),1,color=tones[3],width=.5)
 text(p,X+ww+2,Y+H*.66,f'{lab} %',7);xx=X+W+34;ww=W*flab/60;rect(p,(xx,Y,xx+ww,Y+H*.8),yellow);text(p,xx+ww+2,Y+H*.66,f'{flab} %',7)
for xx,title in [(X,'% des 2 579 fonctions rouges'),(X+W+34,'% des 1 140 fonctions jaunes')]:ticks(p,xx,B.y1-23,W,range(0,61,10),60);text(p,xx+W/2,B.y1-13,title,7,align='center')
legend(p,B.x0,B.y1-2,['bloquée par la dimension','premier blocage (ordre conventionnel)'],[red,tones[3]],193)
# Figure 18.
p,B=figure(63);X=B.x0+183;cw=66;H=(B.height-50)/19;raw="""CIRCUIT DE RÉFÉRENCE
Moyen de transport disponible et fonctionnel|29 + 66|160
Contact préalable avant transfert|45 35 20|160
Destination de référence identifiée|100 - -|160
EAU, HYGIÈNE ET ASSAINISSEMENT
Points d’eau fonctionnels dans les services|22 20 57|157 (U = 3)
Continuité de l’eau sur trois mois|65 11 24|160
Eau disponible en quantité suffisante|52 26 22|160
Continuité du lavage des mains|75 13 11|149 (U = 11)
Dispositif de lavage des mains (eau et savon)|59 33 8|158 (U = 2)
ÉLECTRICITÉ
Source de secours fonctionnelle|40 11 49|157 (U = 3)
Électricité disponible de manière stable|56 16 29|160
Continuité de l’électricité sur trois mois|64 7 29|160
Source d’électricité existante|79 - 21|160
COMMUNICATION
Continuité de la communication sur trois mois|84 + 10|153 (U = 7)
Moyens essentiels fonctionnels le jour de la visite|64 29 7|156 (U = 1)
Au moins un moyen de communication existant|98 - +|160"""
for k,name in enumerate(['Vert','Jaune','Rouge']):text(p,X+(k+.5)*cw,B.y0+10,name,8,align='center')
for j,row in enumerate(raw.splitlines()):
 Y=B.y0+15+j*H
 if '|' not in row:text(p,B.x0,Y+H*.7,row,8,green,True);line(p,X,Y+H*.5,B.x1,Y+H*.5,(.83,.87,.84));continue
 cat,vals,K=row.split('|');text(p,X-4,Y+H*.68,cat,7.3,align='right');
 for k,(v,c) in enumerate(zip(vals.split(),[green,yellow,red])):mark(p,X+k*cw,Y,cw-3,H*.76,v,c)
 text(p,X+3*cw+3,Y+H*.68,'K = '+K,7)
ticks(p,X,B.y1-24,3*cw,range(0,121,20),120);text(p,B.x0+B.width/2,B.y1-13,'% des évaluations calculables (Vert + Jaune + Rouge = 100)',8,align='center');legend(p,B.x0,B.y1-2,['Vert — opérationnelle','Jaune — réalisable, instable','Rouge — non réalisable'],[green,yellow,red],157)
