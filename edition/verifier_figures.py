"""Rendu comparatif des 21 figures antérieures, sans inclure la prose hors figure."""
import glob,subprocess
from pathlib import Path
import pymupdf as m
source=m.open(glob.glob('Rapport_Diagnostic*.pdf')[0]);avant=m.open(stream=subprocess.check_output(['git','show','405348f:edition/Rapport_epreuve.pdf']),filetype='pdf');apres=m.open(Path(__file__).with_name('Rapport_epreuve.pdf'))
for n in [27,29,34,35,36,37,38,43,44,48,49,51,52,53,54,58,61,63,68,77,81]:
    options=dict(clip=m.Rect(source[n-1].get_image_info()[0]['bbox']),matrix=m.Matrix(2,2));assert avant[n-1].get_pixmap(**options).samples==apres[n-1].get_pixmap(**options).samples,n
print('21 figures antérieures : rendus identiques pixel par pixel à 144 ppp.')
