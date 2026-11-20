"""Rapprochement des intitulés imprimés et des légendes du corps du diagnostic."""
import re

def lire_listes(doc):
    pages=[]
    for p in doc:
        raw=p.get_text();idx=[i for i,c in enumerate(raw) if not c.isspace()];pages.append((''.join(raw[i] for i in idx),raw,idx))
    result=[]
    for n in (6,7,8):
        t=pages[n-1][0];matches=list(re.finditer(r'(Figure|Tableau)(A?\d+):',t))
        for j,m in enumerate(matches):
            row=t[m.end():matches[j+1].start() if j+1<len(matches) else None];row=re.sub(r'(Listedestableaux|Tableauxdesannexes)$','',row);end=re.search(r'(Erreur!Signetnondéfini\.|\d+)$',row);assert end,row
            title=row[:end.start()].rstrip('.');wanted=m.group()+title
            for k,(flat,raw,idx) in enumerate(pages[8:],9):
                a=flat.find(wanted)
                if a>=0:
                    body=' '.join(raw[idx[a+len(m.group())]:idx[a+len(wanted)-1]+1].split());break
            else:
                yield n,m.group(1),m.group(2),title,None;continue
            yield n,m.group(1),m.group(2),body,k
