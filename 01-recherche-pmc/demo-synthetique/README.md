# Démonstration synthétique — scoring de candidats

Cette démonstration illustre un score d'identité simple. Elle ne contacte aucun site et
n'utilise aucune donnée d'entreprise.

## Exécution

```bash
python3 demo_pmc.py
python3 -m unittest test_demo_pmc.py
```

Le programme compare un produit recherché à plusieurs candidats fictifs. Il affiche les
preuves, les pénalités, le score et la décision.

Le score est volontairement pédagogique. Il ne reprend pas les seuils ou les règles du
pipeline réalisé pendant le stage.

