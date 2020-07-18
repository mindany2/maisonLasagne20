from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Relais_arduino import Relais_arduino, MESSAGE_MASTER


class Gestionnaire_de_cartes:
    """
    Ceci est une classe static
    """
    liste_carte_relais = []
    liste_carte_triac = []


    @classmethod
    def get_relais(self, carte, indice_relais):
        if carte != "arduino":
            indice_carte = int(carte)
            return self.liste_carte_relais[indice_carte-1].get_relais(indice_relais)

    @classmethod
    def get_triac(self, indice_carte, indice_triac):
        return self.liste_carte_triac[indice_carte-1].get_triac(indice_triac)


    @classmethod
    def configure(self, carte):
        print(carte)
        if isinstance(carte, Carte_triac):
            self.liste_carte_triac.append(carte)
        elif isinstance(carte, Carte_relais):
            self.liste_carte_relais.append(carte)
