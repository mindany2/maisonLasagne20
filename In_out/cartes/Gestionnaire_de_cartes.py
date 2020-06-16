from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Relais_arduino import Relais_arduino, MESSAGE_MASTER


class Gestionnaire_de_cartes:
    """
    Ceci est une classe static
    """
    liste_carte_relais = [Carte_relais(1, 0x21), Carte_relais(2, 0x22)]
    liste_carte_triac = [Carte_triac(1), Carte_triac(2),Carte_triac(3), Carte_triac(4)]
    liste_relais_arduino = [ Relais_arduino(MESSAGE_MASTER.relais_led_escalier_on, MESSAGE_MASTER.relais_led_escalier_off) ]


    @classmethod
    def get_relais(self, carte, indice_relais):
        if carte == "arduino":
            return self.liste_relais_arduino[indice_relais-1]
        indice_carte = int(carte)
        return self.liste_carte_relais[indice_carte-1].get_relais(indice_relais)

    @classmethod
    def get_triac(self, indice_carte, indice_triac):
        return self.liste_carte_triac[indice_carte-1].get_triac(indice_triac)

