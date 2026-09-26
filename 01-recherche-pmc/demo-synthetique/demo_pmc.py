"""Mini-démonstration publique d'un scoring d'identité produit.

Toutes les données et règles sont fictives et ont été écrites pour ce portfolio.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path


def normaliser(texte: str) -> set[str]:
    texte = unicodedata.normalize("NFD", texte.casefold())
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return set(re.findall(r"[a-z0-9]+", texte))


@dataclass(frozen=True)
class Produit:
    nom: str
    marque: str
    format: str
    ean: str
    prix: float | None = None


@dataclass(frozen=True)
class Evaluation:
    candidat: str
    score: int
    decision: str
    preuves: tuple[str, ...]
    alertes: tuple[str, ...]


def evaluer(reference: Produit, candidat: Produit) -> Evaluation:
    score = 0
    preuves: list[str] = []
    alertes: list[str] = []

    if reference.ean and candidat.ean == reference.ean:
        score += 55
        preuves.append("EAN identique")
    elif candidat.ean:
        score -= 35
        alertes.append("EAN différent")

    if normaliser(reference.marque) == normaliser(candidat.marque):
        score += 20
        preuves.append("marque identique")
    else:
        score -= 25
        alertes.append("marque différente")

    communs = normaliser(reference.nom) & normaliser(candidat.nom)
    union = normaliser(reference.nom) | normaliser(candidat.nom)
    similarite = len(communs) / len(union) if union else 0
    score += round(20 * similarite)
    preuves.append(f"similarité du nom {similarite:.0%}")

    if normaliser(reference.format) == normaliser(candidat.format):
        score += 15
        preuves.append("conditionnement identique")
    else:
        score -= 30
        alertes.append("conditionnement incompatible")

    score = max(0, min(100, score))
    if score >= 80 and not alertes:
        decision = "proposition automatique"
    elif score >= 55:
        decision = "revue humaine"
    else:
        decision = "rejet"

    return Evaluation(candidat.nom, score, decision, tuple(preuves), tuple(alertes))


def charger(path: Path) -> tuple[Produit, list[Produit]]:
    donnees = json.loads(path.read_text(encoding="utf-8"))
    return Produit(**donnees["reference"]), [Produit(**c) for c in donnees["candidats"]]


def main() -> None:
    reference, candidats = charger(Path(__file__).with_name("produits_fictifs.json"))
    evaluations = sorted(
        (evaluer(reference, candidat) for candidat in candidats),
        key=lambda evaluation: evaluation.score,
        reverse=True,
    )
    print(json.dumps([asdict(e) for e in evaluations], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

