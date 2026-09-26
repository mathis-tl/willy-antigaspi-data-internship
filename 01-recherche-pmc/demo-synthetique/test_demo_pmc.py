import unittest

from demo_pmc import Produit, evaluer


REFERENCE = Produit(
    nom="Purée de pomme bio quatre gourdes",
    marque="Verger Démo",
    format="4 x 100 g",
    ean="9999999999999",
)


class TestScoring(unittest.TestCase):
    def test_candidat_identique_est_propose(self):
        resultat = evaluer(REFERENCE, REFERENCE)
        self.assertEqual(resultat.score, 100)
        self.assertEqual(resultat.decision, "proposition automatique")

    def test_unite_seule_n_est_pas_auto_proposee(self):
        candidat = Produit(
            nom="Purée de pomme bio une gourde",
            marque="Verger Démo",
            format="100 g",
            ean="8888888888888",
        )
        resultat = evaluer(REFERENCE, candidat)
        self.assertNotEqual(resultat.decision, "proposition automatique")
        self.assertIn("conditionnement incompatible", resultat.alertes)

    def test_marque_differente_est_penalisee(self):
        candidat = Produit(
            nom=REFERENCE.nom,
            marque="Autre Marque",
            format=REFERENCE.format,
            ean="7777777777777",
        )
        resultat = evaluer(REFERENCE, candidat)
        self.assertIn("marque différente", resultat.alertes)


if __name__ == "__main__":
    unittest.main()

