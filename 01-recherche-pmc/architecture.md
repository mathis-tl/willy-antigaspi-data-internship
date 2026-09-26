# Architecture simplifiée : recherche PMC

```mermaid
flowchart TD
    A[Produit de l'offre] --> B[Normalisation contrôlée]
    B --> C[Recherche EAN et texte]
    C --> D[Sources catalogue et API]
    D --> E[Extraction des preuves]
    E --> F{Identité cohérente ?}
    F -->|Non| G[Rejet ou revue]
    F -->|Oui| H[Extraction du prix]
    H --> I[Score et confiance]
    I --> J{Seuil atteint ?}
    J -->|Oui| K[Proposition automatique]
    J -->|Non| L[Revue humaine]
    K --> M[(Persistance)]
    L --> M
    M --> N[Affichage dans l'outil acheteur]
```

## Responsabilités

| Brique | Responsabilité |
| --- | --- |
| Collecte | Obtenir plusieurs candidats auprès de sources différentes. |
| Normalisation | Comparer des textes et formats exprimés différemment. |
| Filtres | Rejeter les incompatibilités certaines. |
| Scoring | Agréger des preuves d'identité explicables. |
| Extraction | Lire le prix du candidat validé. |
| Persistance | Conserver le résultat, sa source et sa confiance. |
| Revue | Permettre à un acheteur de trancher les cas ambigus. |

## Point de conception principal

```text
Identité du produit d'abord → prix ensuite
```

Le système évite de choisir un candidat uniquement parce que son prix semble plausible.

