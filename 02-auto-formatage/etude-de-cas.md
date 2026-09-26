# Auto-formatage des offres fournisseurs

## Le problème

Les offres fournisseurs arrivaient sous forme de fichiers Excel très différents :

- noms et ordre de colonnes variables ;
- en-têtes déplacés ou répartis sur deux lignes ;
- unités hétérogènes ;
- plusieurs onglets produit ;
- légendes de marques ;
- cellules fusionnées ou erreurs Excel ;
- lignes de sous-total et résidus de mise en forme.

Les acheteurs devaient remettre ces fichiers dans un gabarit commun avant de pouvoir
lancer l'analyse. Le travail était répétitif et une feuille Google partagée limitait le
travail simultané.

## Le choix principal

J'ai séparé les responsabilités :

> **L'IA lit, le code garantit, l'humain tranche.**

- un modèle de langage identifie la structure et les colonnes ;
- le code relit les cellules et contrôle les données vérifiables ;
- l'acheteur corrige uniquement les exceptions visibles.

Cette séparation évite deux extrêmes : un parseur figé incapable de comprendre un
nouveau fournisseur, et une IA libre d'inventer ou de modifier une valeur sensible.

## La solution

Le pipeline :

1. vérifie le format du fichier ;
2. détecte les onglets susceptibles de contenir des produits ;
3. construit un aperçu textuel avec les coordonnées des cellules ;
4. demande un mapping structuré ;
5. extrait mécaniquement les valeurs ;
6. complète seulement certains champs restés vides ;
7. contrôle les réponses ;
8. normalise les EAN, dates, poids, TVA et nombres ;
9. rapproche les doublons entre onglets ;
10. attribue une confiance par ligne ;
11. crée une Google Sheet dédiée et conserve les onglets bruts.

## Garde-fous

### Aucune ligne perdue silencieusement

Toute ligne non vide doit être classée comme produit, en-tête ou ligne ignorée. Une
ligne oubliée est réinjectée dans le résultat et marquée comme bloquante.

### Données sensibles contrôlées par le code

- checksum de l'EAN ;
- dates impossibles ou ambiguës ;
- nombres et entiers ;
- poids positif et unités ;
- TVA autorisée ;
- erreurs `#REF!` et `#VALUE!` ;
- preuve textuelle pour le contenant en verre ;
- fragment exact du libellé pour un poids inféré.

### Fusion prudente des onglets

Deux lignes ne sont fusionnées que si leur identité et les autres colonnes sont
compatibles. Les lots distincts restent séparés et les conflits sont visibles.

## Statuts de relecture

| Statut | Sens |
| --- | --- |
| Vert | Aucun problème détecté. |
| Orange | Information complémentaire ambiguë ou à vérifier. |
| Rouge | Donnée indispensable absente ou invalide. |

Un fichier peut être correctement traité tout en contenant des lignes rouges. Le rouge
est une information destinée à l'acheteur, pas un échec technique du fichier entier.

## Ce que j'ai réalisé

- pipeline Python de lecture et transformation ;
- détection d'en-têtes sur plusieurs lignes ;
- mapping structuré par LLM ;
- extraction et normalisation déterministes ;
- validations métier ;
- traitement multi-onglets et déduplication ;
- harnais de comparaison avec une référence humaine ;
- tests anti-invention et anti-perte ;
- client Google Drive/Sheets ;
- bundle Python compatible avec Retool ;
- file de formatage asynchrone ;
- watchdog et reprise des jobs interrompus ;
- documentation d'utilisation et de débogage.

## Résultats

Sur le premier lot de référence, les 14 lignes ont été retrouvées et les colonnes
indispensables ont atteint 100 % de justesse après correction de la référence humaine.
Aucune ligne n'a été perdue.

Une offre de 181 lignes a ensuite révélé un timeout. Le découpage des appels
sémantiques en lots de 40 a permis de terminer le traitement en production sans timeout.

## Difficultés

- grande variété des fichiers ;
- vérité terrain humaine parfois incorrecte ;
- ambiguïtés de dates et d'unités ;
- doublons entre onglets ;
- gros fichiers et durée des appels externes ;
- différence entre code source testé et bundle réellement déployé ;
- nécessité de rester compatible avec le workflow d'analyse existant.

## Ce que j'ai appris

- répartir les responsabilités entre IA, code et humain ;
- transformer les incidents réels en tests de régression ;
- privilégier un résultat incomplet mais signalé à une correction silencieuse ;
- tester le contrat entre deux systèmes, pas seulement chaque système isolément ;
- concevoir la reprise et le diagnostic dès le début d'un traitement asynchrone.

## Limites et suites possibles

- prise en charge des `.xlsx` uniquement ;
- aperçu borné pour les onglets extrêmement longs ;
- enrichissement continu du corpus de test ;
- notifications de fin de traitement ;
- automatisation future de la réception des pièces jointes par mail.

