# Démonstration synthétique : normalisation d'une offre

Cette démonstration transforme un CSV fictif en CSV normalisé. Elle illustre :

- le mapping de colonnes ;
- la conversion d'un poids vers les kilogrammes ;
- un contrôle simplifié de l'EAN ;
- la production d'un statut et de raisons lisibles.

Elle ne contient ni LLM, ni Google Sheets, ni règle confidentielle.

## Exécution

```bash
python3 demo_formatage.py
python3 -m unittest test_demo_formatage.py
```

Le fichier `offre_formatee.csv` est créé dans le même dossier.

