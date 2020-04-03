from utils.In_out.controle.Carte_triac import Carte_triac
from utils.In_out.controle.Carte_relais import Carte_relais


class Controle:
    """
    Ceci est une classe static
    """
    liste_carte_relais = [Carte_relais(1, 0x21, 0x13), Carte_relais(2, 0x21, 0x12)]
    liste_carte_triac = [Carte_triac(1), Carte_triac(2)]


    @classmethod
    def get_relais(self, indice_carte, indice_relais):
        return self.liste_carte_relais[indice_carte-1].get_relais(indice_relais)

    @classmethod
    def get_triac(self, indice_carte, indice_triac):
        return self.liste_carte_triac[indice_carte-1].get_triac(indice_triac)

if  __name__ == "__main__":
    Controle()
