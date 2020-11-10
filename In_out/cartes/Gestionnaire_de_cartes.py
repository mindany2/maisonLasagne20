from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Relais_GPIO import Relais_GPIO
from In_out.cartes.relais.Relais_arduino import Relais_arduino, MESSAGE_MASTER
from In_out.dmx.controleurs.Controleur_dmx import Controleur_dmx


class Gestionnaire_de_cartes:
    """
    Ceci est une classe static qui permet de gérer les différentes cartes
    ajouter sur le rpi
    """
    liste_carte_relais = []
    liste_carte_triac = []
    dmx = None

    @classmethod
    def get_dmx(self):
        return self.dmx

    @classmethod
    def get_relais(self, carte, indice_relais):
        indice_relais = int(indice_relais)
        try:
            if carte == "gpio":
                # l'indice du relais joue le role du port gpio
                return Relais_GPIO(indice_relais)
            else:
                # c'est une carte
                indice_carte = int(carte)
                return self.liste_carte_relais[indice_carte-1].get_relais(indice_relais)
        except:
            return None

    @classmethod
    def get_triac(self, indice_carte, indice_triac):
        return self.liste_carte_triac[indice_carte-1].get_triac(indice_triac)


    @classmethod
    def configure(self, carte):
        if isinstance(carte, Carte_triac):
            self.liste_carte_triac.append(carte)
        elif isinstance(carte, Carte_relais):
            self.liste_carte_relais.append(carte)
        elif isinstance(carte, Controleur_dmx):
            self.dmx = carte

