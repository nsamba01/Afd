"""Fonds et séparateurs vectoriels ; conserver les cellules de texte du diagnostic."""
# Limites des lignes et des colonnes (points PDF), relevées sur les bordures du
# rapport. Les rectangles supplémentaires de Word sont des trames, pas des lignes.
TABLEAUX={
 9:([58.6,123.2,536.8],[84,100.1,116.1,132,148.1,164.1,180,196.1,212.1,228,244.1,260.1,276.1,292.1,308.1,324.1,340.1,356.1,372,388.1,404.1,420,447.9,464,479.9,495.9,512,528,543.9,560,576,591.9,608,638.4,654.3,670.4,686.4,702.3,718.4,734.4,750.3,766.4,783.4]),
 10:([58.6,124.1,536.8],[62,78,94.1,110.1,126,142.1,158.1,174,190.1,206.1,222,238.1,254.1,270.1,286.1,302.1,318.1,334.1,350.1,366,382.1,398.1,414,430.1,446.1,462.1,478.1,494.1,510,526.1,543.1]),
 17:([56.6,290.2,400.3,510.4],[428.6,449.8,470.7,491.7,512.6,533.5,554.5,575.8]),
 22:([56.6,82.7,315.8,513.8],[150.1,165.3,180,208.7,237.5,266.3,295.1,323.9,352.7,381.8]),
 75:([46.8,201.2,323.2,353,438,548.6],[259.3,291.8,311.8,344.2,364.1,384.2,404.1,436.5,456.4,476.5,521.3,553.8,573.7,606.2,638.6,658.9]),
 84:([56.9,162,254.5,349.6,444.5,547],[189.7,216.3,253.7,280.2,317.7,355.1,392.6,430,457]),
}
for n,ys in [(71,[83.1,118.1,226.4,333.1,458.6]),(72,[62.1,97.1,183.9,299.7,410.1,497.3]),(73,[62.1,97.1,169.9,256.6,361.6,476.4])]:TABLEAUX[n]=([57,168.6,262.2,376.5,561.1,727.5,791.5],ys)

def fond_tableau(p,n):
    xs,ys=TABLEAUX[n];patches=[d['fill'] for d in R[48].get_drawings() if d['fill'] and d['rect'].width>400];header,shade1,shade2=patches[:3]
    rect(p,(xs[0]-.6,ys[0]-.6,xs[-1]+.6,ys[-1]+.6),white)
    for j,(top,bottom) in enumerate(zip(ys,ys[1:])):
        rect(p,(xs[0],top,xs[-1],bottom),header if j==0 else (shade1,shade2)[(j-1)%2])
        if j:line(p,xs[0],top,xs[-1],top,white,.7)
    for x in xs[1:-1]:line(p,x,ys[0],x,ys[-1],white,.7)

def chapitre_affine(p,exempts):
    # Free 30 pt below the model's title without clipping or moving any section
    # to a different page. Keep the masthead and 36 pt title at their native size.
    from itertools import groupby
    h=p.rect.height
    for move,group in groupby(p.get_contents(),key=lambda ref:ref not in exempts):
        ids=list(group)
        if move:
            a,b=ids[0],ids[-1];D.update_stream(a,('q 1 0 0 .96 0 %.5f cm\n'%(.04*h-33.1)).encode()+D.xref_stream(a));D.update_stream(b,D.xref_stream(b)+b'\nQ\n')
