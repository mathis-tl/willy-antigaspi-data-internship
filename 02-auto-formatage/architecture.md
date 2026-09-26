# Architecture simplifiée : auto-formatage

```mermaid
flowchart TD
    A[Fichier fournisseur] --> B[Stockage privé]
    B --> C[File de formatage]
    C --> D[Lecture des onglets]
    D --> E[Mapping de la structure]
    E --> F[Extraction mécanique]
    F --> G[Complétion limitée]
    G --> H[Contrôles déterministes]
    H --> I[Déduplication multi-onglets]
    I --> J[Statuts par ligne]
    J --> K[Google Sheet dédiée]
    K --> L[Relecture humaine]
    L --> M[File d'analyse]
```

## Répartition des responsabilités

| Acteur | Rôle |
| --- | --- |
| IA | Lire une structure nouvelle et proposer un mapping. |
| Code | Copier les cellules, normaliser et vérifier. |
| Acheteur | Arbitrer les lignes orange et rouges. |
| Orchestrateur | Réserver les jobs, gérer les tentatives et stocker le résultat. |

## États d'un job

```mermaid
stateDiagram-v2
    [*] --> Upload
    Upload --> EnAttente
    EnAttente --> EnCours
    EnCours --> Termine
    EnCours --> EnAttente: reprise automatique
    EnCours --> Erreur: échec final
    Termine --> [*]
    Erreur --> [*]
```

## Sortie d'une ligne

```text
15 colonnes métier
+ statut de confiance
+ raisons détaillées
+ numéro de ligne source
```

