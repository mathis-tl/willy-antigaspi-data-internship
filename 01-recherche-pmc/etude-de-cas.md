# Recherche automatique de prix publics comparables

## Le problème

Pour analyser une offre fournisseur, un acheteur doit comparer le prix proposé avec un
prix public. Cette recherche était en grande partie manuelle et son résultat n'était pas
toujours conservé.

Chercher un EAN sur Internet ne suffit pas. Un résultat peut correspondre :

- à un lot au lieu d'une unité ;
- à une contenance différente ;
- à une variante proche ;
- à un vendeur tiers ;
- à un prix barré ou une promotion ;
- à un produit qui n'est plus disponible.

Le risque principal n'était donc pas l'absence de résultat, mais un mauvais produit
présenté comme une correspondance fiable.

## Ma démarche

J'ai commencé par construire des sourceurs et un benchmark avec validation humaine. Le
but était de mesurer séparément :

- la couverture : combien de produits obtiennent un candidat ;
- la précision : combien de candidats correspondent réellement au bon produit ;
- la qualité du prix : le prix extrait est-il comparable et actuel ?

Les premiers essais ont montré qu'une approche générique pouvait obtenir une bonne
couverture tout en produisant trop de faux positifs. J'ai ensuite privilégié les données
structurées et les API utilisées directement par certains sites marchands.

## La solution retenue

Le pipeline fonctionne comme une cascade de preuves :

1. normalisation contrôlée du nom ;
2. recherche de candidats par EAN et par texte ;
3. collecte de données structurées ;
4. vérification de l'EAN, de la marque et du conditionnement ;
5. utilisation de l'image comme preuve complémentaire ;
6. scoring de l'identité du produit ;
7. extraction du prix seulement après validation de l'identité ;
8. classement des candidats ;
9. proposition automatique ou envoi en revue humaine.

Le prix n'est volontairement pas la preuve principale. Deux produits différents peuvent
avoir un prix proche, alors qu'une différence de marque ou de format suffit à rendre la
comparaison incorrecte.

## Ce que j'ai réalisé

- sourceurs spécialisés et génériques ;
- analyse des requêtes réseau de sites marchands ;
- canonicalisation des URL ;
- extraction de données structurées ;
- pipeline de scoring explicable ;
- détection de lots, coffrets et formats incompatibles ;
- consensus d'image avec garde-fous textuels ;
- runners de benchmark et rapports de revue ;
- cache, retries et limitation de concurrence ;
- flow de production orchestré avec Prefect ;
- persistance dans Supabase ;
- intégration du prix, de la confiance, de l'URL et de l'image dans Retool.

## Exemple de décision

Pour une recherche « Purée de pomme bio 4 × 100 g », trois candidats peuvent être
trouvés :

| Candidat | EAN | Marque | Format | Décision |
| --- | --- | --- | --- | --- |
| Purée de pomme bio 4 × 100 g | identique | identique | identique | candidat fort |
| Purée de pomme bio 100 g | différent | identique | unité seule | rejet : lot incompatible |
| Purée pomme-poire bio 4 × 100 g | différent | identique | identique | rejet : variante différente |

Cet exemple illustre pourquoi un score doit combiner plusieurs preuves.

## Résultats

Un benchmark de 100 produits revu manuellement a réparti les résultats en trois groupes :

- 56 bons produits avec un bon prix ;
- 28 bons produits dont le prix restait à vérifier ;
- 16 mauvais produits.

Ce benchmark a orienté le projet vers davantage de prudence. Les cas douteux restent
visibles avec leurs candidats, mais ne sont pas automatiquement utilisés.

## Difficultés

- protections anti-bot et limitations par domaine ;
- prix chargés dynamiquement ;
- promotions et prix barrés ;
- produits délistés ou en rupture ;
- différences entre unité et multipack ;
- données structurées variables selon les marchands ;
- absence de vérité terrain parfaite.

## Ce que j'ai appris

- mesurer avant de généraliser ;
- séparer couverture et précision ;
- rendre un score explicable ;
- conserver les preuves qui ont produit la décision ;
- préférer « aucun résultat » à un faux positif silencieux ;
- prévoir une revue humaine pour les situations réellement ambiguës.

## Limites et suites possibles

- améliorer la distinction entre prix normal et promotion ;
- ajouter de nouvelles sources sans dégrader la précision ;
- mieux traiter les variantes JavaScript ;
- suivre la fraîcheur des prix ;
- construire un benchmark continu à partir des validations des acheteurs.

