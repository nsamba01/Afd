# Épreuve de composition — contrôle de livraison

**Statut : épreuve pour validation, pas un bon à tirer.** Le PDF de 151 pages conserve la pagination du rapport de diagnostic. Aucun texte, logo ni photographie de Md_ref n’a été transféré dans le rapport. La couverture emploie les trois marques du diagnostic, son titre et sa date, avec le traitement vert, blanc et or et l’alignement à droite du modèle. Aucun visuel photographique n’a été inventé pour remplacer la photographie du modèle.

## Contrôles effectués

- Ouverture et rendu des 151 pages ; aucune page entièrement blanche, aucun mot détecté hors du format de page.
- Comparaison page par page du flux textuel extrait avec le PDF source, hors graphiques reconstruits et sommaire recomposé : aucun écart après normalisation Unicode, des espaces et des puces. Cette vérification comprend les cellules textuelles des tableaux et les annexes ; elle ne mesure pas la lisibilité d’une épreuve papier.
- Vérification des 54 entrées du sommaire : titre présent sur la page indiquée, signet et lien interne. Les intitulés sont ceux du rapport ; les numéros figurent à gauche comme dans Md_ref.
- Les 21 figures sont constituées de texte et d’objets vectoriels. Le rendu des 21 pages concernées n’appelle aucune image matricielle. Le texte des figures est sélectionnable.
- Les polices Univers Condensed et Univers Bold Condensed proviennent des sous-ensembles incorporés au modèle. Les glyphes indisponibles dans ces sous-ensembles passent dans une police de secours incorporée. Les listes des pages 6 à 8 ont été intégralement recomposées à partir des intitulés du diagnostic et vérifiées contre les légendes du corps du rapport.
- Les tableaux conservent les positions, les lignes, les colonnes et les codes couleur sémantiques du diagnostic. La palette des en-têtes et des filets a été harmonisée. Les sauts entre pages et les répétitions d’en-têtes sont ceux de la source, et non le résultat d’une nouvelle composition automatique de tableaux.

## Lecture et limites des figures

Aucun pourcentage n’a été obtenu en mesurant la longueur d’une barre sur l’image. Les effectifs, matrices et étiquettes publiés ont été retranscrits. Lorsque le rapport donne les effectifs, ceux-ci déterminent les longueurs ; les étiquettes conservent les arrondis publiés. Exemples : figure 2 / tableau 7 ; figure 13 / tableau A58 ; figure 20 / tableau A62 (les sept étapes de la figure, non les neuf du tableau). Pour la figure 8, la compatibilité des effectifs entiers avec le dénominateur et les pourcentages arrondis est testée ; une seule solution est admise.

**Un petit cercle évidé représente un segment visible dont la valeur n’est pas chiffrée sur la figure source. Il ne représente pas zéro.** Dans les figures 3, 5, 6, 7, 9, 10 et 18, les séries sont présentées en colonnes distinctes afin que les valeurs publiées puissent être représentées sans inventer la largeur d’un segment non étiqueté. Dans la figure 12, le tableau 18 renseigne les principaux effectifs de premier blocage, mais pas toute la sous-série des dimensions supplémentaires. La précision de cette sous-série reste à valider. Dans la figure 6, certaines valeurs publiées totalisent plus de 100 % (p. ex. 16 et 89) : elles ont été conservées, et non corrigées ou ramenées à 100 %.

**Avant diffusion officielle :** rapprocher ces huit figures de leurs séries de calcul non arrondies, contrôler les petits dénominateurs et valider les tableaux denses sur une impression A4 à taille réelle. Aucune affirmation de conformité PDF/X ni d’approbation institutionnelle n’est faite.

## Sources modifiables

L’archive `Sources_editables.zip` contient une page SVG éditable par page du rapport (texte et tracés), ainsi que les scripts de production et de contrôle. Pour une retouche isolée, ouvrir le SVG concerné dans un éditeur vectoriel. L’apparence du texte dans un éditeur dépend des polices installées ; le PDF est la référence de rendu. Les textes positionnés ne constituent pas un document Word à pagination fluide.

Pour régénérer le PDF dans le dépôt : depuis la racine, avec Python 3, PyMuPDF, fonttools et les polices DejaVu Sans installés, exécuter `python edition/produire.py`, puis `python edition/verifier.py`. Les deux PDF d’entrée doivent rester à la racine. Les données transcrites et les tracés des figures se trouvent dans `edition/figures.py`.

## Révision des titres et de l’infographie

La couverture reprend la taille de titre de Md_ref (50 pt, interligne 55 pt) et la ligne secondaire or de 40 pt. Le diagnostic ne comporte pas de sous-titre de couverture distinct : la ligne « Kinshasa, Octobre 2026 » tient cette place. Les ouvertures de chapitre utilisent le grand titre vert condensé ; les intertitres numérotés utilisent la variante grasse, avec adaptation pour les lignes longues ou serrées.

Page 26, la phrase décrivant les 160 établissements a été composée sous forme de panneau et de trois barres d’effectifs (101, 22, 37). Page 27, un bandeau proportionnel relie les trois résultats déjà imprimés (68,4 %, 30,2 %, 1,4 %). Ces éléments n’ajoutent ni intitulé analytique ni résultat. Le contrôle `Controle_par_page.csv` détaille le périmètre du rapprochement pour chacune des 151 pages. Il s’agit d’un contrôle numérique, et non d’un bon à tirer papier ou d’une validation indépendante des données non publiées des figures.

## Gabarit continu et nouvelles infographies

La couverture possède un fond géométrique vectoriel bicolore. Les 150 pages intérieures, y compris le sommaire, les listes, les tableaux en paysage, la bibliographie et les annexes, portent un repère de tranche recto/verso et un bandeau de navigation vert avec le titre de la section et le folio.

La page 13 recompose les cinq messages du diagnostic en cinq cartes reliées, chacune identifiée par un pictogramme vectoriel. Les phrases originales restent intégrales, y compris la réserve d’interprétation en pied de composition. Aux pages 100, 105, 110, 115, 119, 124, 129 et 134, un nouveau graphique provincial rapproche la part de fonctions rouges et celle des **fonctions vitales** rouges. Les deux barres utilisent une échelle commune de 0 à 100 %, mais portent sur deux populations différentes et ne doivent pas être additionnées. Les valeurs sont extraites des phrases « Position » de chaque province ; la présentation compacte ou étendue dépend de la place des tableaux sur la page.

Les nouvelles zones de navigation et de données sont contrôlées séparément du texte courant (`zones_design.json` et `verifier.py`). La comparaison du corps du rapport reste effectuée sur les 151 pages selon les modalités précisées ci-dessus. Les limites des huit figures dont des valeurs ne sont pas imprimées dans le document source restent inchangées.

## Révision des listes et lectures graphiques complémentaires

Les pages 6 à 8 sont des index de texte vectoriel, non des reproductions de la liste Word. Le folio de destination est placé à gauche, puis viennent le numéro de figure ou de tableau et la légende. Le script rapproche les 21 figures, 37 tableaux et 64 tableaux annexes des légendes imprimées, puis crée un lien par entrée. Le renvoi non défini du tableau 29 est remplacé par sa destination vérifiée, page 70.

Trois lectures graphiques non numérotées accompagnent des données déjà présentes : rôle des douze dimensions sur une échelle de 71 spécifications (p. 23) ; indisponibilité au jour de la visite et ruptures prolongées dans deux groupes distincts (p. 55) ; sept événements déclarés au cours des trois derniers mois, présentés séparément et non additionnés (p. 64). Les tableaux et paragraphes restent intégralement présents.

## Révision du gabarit : navigation uniquement en haut

Cette révision remplace le bandeau de pied et les repères de tranche décrits dans les révisions précédentes. Le folio et le titre courant sont désormais en haut des pages intérieures, y compris sur les matrices en paysage. Les vingt derniers points de chaque page intérieure sont contrôlés après rendu : aucune encre de pied de page. La couverture reste sans folio.

Les ouvertures de Préface, Remerciements, Abréviations et acronymes, Résumé exécutif, Introduction, Approche méthodologique, Résultats, Discussion, Conclusion et recommandations, Bibliographie et Annexes reprennent le titre vert de 36 pt des listes, sa marge gauche, sa ligne de base et son filet à amorce or. La zone de composition sous le titre est adaptée sans modifier la pagination ni les destinations des liens.

Les tableaux des pages 9–10, 17, 22, 71–73, 75 et 84 sont rhabillés sur la base du tableau de la page 49 de Md_ref : fond vert institutionnel pour les titres de colonnes, deux trames vert-gris alternées et séparateurs blancs. Le texte et les dimensions des colonnes sont ceux du diagnostic. L’en-tête est répété sur les deux pages du glossaire et les trois pages de la matrice. Les scripts et les SVG de l’archive correspondent à cette version.
