import unittest

from demo_formatage import checksum_ean13_valide, formater_ligne, poids_en_kg


def ligne(**changements):
    base = {
        "Réf": "D-001",
        "Produit": "Boisson pomme bio",
        "Fabricant": "Marque Démo",
        "Code barre": "4006381333931",
        "Format": "750 g",
        "TVA": "5,5",
        "Qté dispo": "120",
    }
    base.update(changements)
    return base


class TestFormatage(unittest.TestCase):
    def test_checksum_ean_connu(self):
        self.assertTrue(checksum_ean13_valide("4006381333931"))
        self.assertFalse(checksum_ean13_valide("4006381333932"))

    def test_conversion_du_poids(self):
        self.assertEqual(poids_en_kg("750 g"), 0.75)
        self.assertEqual(poids_en_kg("1,5 kg"), 1.5)

    def test_ligne_valide_est_verte(self):
        self.assertEqual(formater_ligne(ligne(), 2)["statut"], "VERT")

    def test_ean_invalide_est_rouge(self):
        resultat = formater_ligne(ligne(**{"Code barre": "123"}), 2)
        self.assertEqual(resultat["statut"], "ROUGE")
        self.assertIn("EAN invalide", resultat["raisons"])

    def test_stock_inconnu_est_orange(self):
        resultat = formater_ligne(ligne(**{"Qté dispo": "à confirmer"}), 2)
        self.assertEqual(resultat["statut"], "ORANGE")


if __name__ == "__main__":
    unittest.main()

