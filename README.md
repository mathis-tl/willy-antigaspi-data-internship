# Deux projets data menés chez Willy Anti-Gaspi

Ce dossier présente deux projets réalisés pendant mon stage d'ingénieur en 2026 :

1. la recherche automatique de prix publics comparables (PMC) ;
2. l'auto-formatage d'offres fournisseurs reçues sous forme de fichiers Excel.

Les deux projets répondent au même besoin : aider les acheteurs à exploiter des données
hétérogènes sans masquer les cas incertains.

## Mon rôle

Je suis intervenu sur l'ensemble du cycle de réalisation :

- analyse du besoin avec les utilisateurs ;
- exploration et benchmark de plusieurs approches ;
- conception de l'architecture ;
- développement Python ;
- normalisation et contrôle de données ;
- tests automatisés et cas de régression ;
- orchestration des traitements ;
- intégration dans Retool, Supabase et Google Sheets ;
- canaris de production et documentation de débogage.

## Résultats principaux

### Recherche PMC

- constitution d'un pipeline à plusieurs sources et plusieurs niveaux de preuve ;
- séparation entre identité du produit et extraction du prix ;
- scoring de confiance et revue humaine pour les cas ambigus ;
- intégration des résultats dans l'outil utilisé par les acheteurs ;
- conservation du prix, de l'URL, de la source, de l'image et des candidats alternatifs.

### Auto-formatage

- transformation de fichiers fournisseurs hétérogènes vers un gabarit commun ;
- traitement des classeurs multi-onglets ;
- contrôles déterministes des EAN, dates, poids, TVA et nombres ;
- signalement des lignes incertaines avec trois niveaux de confiance ;
- création d'une Google Sheet dédiée par offre ;
- traitement asynchrone de plusieurs fichiers et suivi des erreurs.

## Contenu du pack

```text
willy-antigaspi-data-internship/
├── README.md
├── CONFIDENTIALITE.md
├── 01-recherche-pmc/
│   ├── etude-de-cas.md
│   ├── architecture.md
│   └── demo-synthetique/
└── 02-auto-formatage/
    ├── etude-de-cas.md
    ├── architecture.md
    └── demo-synthetique/
```

## Lancer les démonstrations

Python 3.10+ uniquement, aucune dépendance externe.

```bash
cd 01-recherche-pmc/demo-synthetique && python3 demo_pmc.py && python3 -m unittest test_demo_pmc.py
cd 02-auto-formatage/demo-synthetique && python3 demo_formatage.py && python3 -m unittest test_demo_formatage.py
```

## À propos des démonstrations

Les démonstrations ont été réécrites spécialement pour ce portfolio. Elles utilisent
uniquement des produits, fichiers et identifiants fictifs. Elles illustrent les choix
d'architecture sans reprendre le code, les données ou les accès de l'entreprise.

## Compétences illustrées

- Python et traitement de données ;
- architecture de pipelines ;
- qualité et validation des données ;
- collecte web et gestion de sources externes ;
- conception de scores explicables ;
- tests et benchmarks ;
- intégration d'IA avec garde-fous déterministes ;
- orchestration et reprise d'erreurs ;
- communication avec des utilisateurs métier.

