"""Mini-démonstration publique de normalisation d'une offre fictive."""

from __future__ import annotations

import csv
import re
from pathlib import Path


COLONNES_SORTIE = (
    "reference",
    "denomination",
    "marque",
    "ean",
    "poids_kg",
    "tva",
    "stock",
    "statut",
    "raisons",
)


def checksum_ean13_valide(ean: str) -> bool:
    if len(ean) != 13 or not ean.isdigit():
        return False
    somme = sum(int(chiffre) * (1 if index % 2 == 0 else 3)
                for index, chiffre in enumerate(ean[:12]))
    cle = (10 - somme % 10) % 10
    return cle == int(ean[-1])


def poids_en_kg(texte: str) -> float | None:
    match = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*(kg|g)\s*", texte, re.I)
    if not match:
        return None
    valeur = float(match.group(1).replace(",", "."))
    return round(valeur if match.group(2).casefold() == "kg" else valeur / 1000, 6)


def entier_ou_vide(texte: str) -> int | None:
    texte = texte.strip()
    return int(texte) if texte.isdigit() else None


def formater_ligne(source: dict[str, str], numero: int) -> dict[str, str]:
    raisons: list[str] = []
    denomination = source["Produit"].strip()
    marque = source["Fabricant"].strip()
    ean = re.sub(r"\D", "", source["Code barre"])
    poids = poids_en_kg(source["Format"])
    stock = entier_ou_vide(source["Qté dispo"])
    tva = source["TVA"].strip().replace(",", ".")

    if not denomination:
        raisons.append("dénomination absente")
    if not marque:
        raisons.append("marque absente")
    if not checksum_ean13_valide(ean):
        raisons.append("EAN invalide")
    if poids is None or poids <= 0:
        raisons.append("poids illisible")
    if tva not in {"5.5", "20"}:
        raisons.append("TVA à vérifier")
    if stock is None:
        raisons.append("stock à vérifier")

    bloquantes = {"dénomination absente", "marque absente", "EAN invalide", "poids illisible"}
    if bloquantes & set(raisons):
        statut = "ROUGE"
    elif raisons:
        statut = "ORANGE"
    else:
        statut = "VERT"

    return {
        "reference": source["Réf"].strip(),
        "denomination": denomination,
        "marque": marque,
        "ean": ean,
        "poids_kg": "" if poids is None else str(poids),
        "tva": tva,
        "stock": "" if stock is None else str(stock),
        "statut": statut,
        "raisons": "; ".join(raisons) or f"ligne source {numero} conforme",
    }


def convertir(source_path: Path, destination_path: Path) -> list[dict[str, str]]:
    with source_path.open(encoding="utf-8", newline="") as fichier:
        lignes = [formater_ligne(ligne, numero)
                  for numero, ligne in enumerate(csv.DictReader(fichier), start=2)]
    with destination_path.open("w", encoding="utf-8", newline="") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=COLONNES_SORTIE)
        writer.writeheader()
        writer.writerows(lignes)
    return lignes


def main() -> None:
    dossier = Path(__file__).parent
    lignes = convertir(dossier / "offre_fictive.csv", dossier / "offre_formatee.csv")
    for ligne in lignes:
        print(f"{ligne['statut']:6} | {ligne['denomination'] or '(sans nom)'} | {ligne['raisons']}")


if __name__ == "__main__":
    main()

