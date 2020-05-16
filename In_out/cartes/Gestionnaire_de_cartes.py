from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.Carte_relais import Carte_relais


class Gestionnaire_de_cartes:
    """
    Ceci est une classe static
    """
    liste_carte_relais = [Carte_relais(1, 0x21), Carte_relais(2, 0x22)]
    liste_carte_triac = [Carte_triac(1), Carte_triac(2),Carte_triac(3)]


    @classmethod
    def get_relais(self, indice_carte, indice_relais):
        return self.liste_carte_relais[indice_carte-1].get_relais(indice_relais)

    @classmethod
    def get_triac(self, indice_carte, indice_triac):
        return self.liste_carte_triac[indice_carte-1].get_triac(indice_triac)

