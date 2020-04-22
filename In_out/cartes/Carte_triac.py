from In_out.cartes.Triac import Triac
from In_out.cartes.Carte import Carte

class Carte_triac:
    """
    Une carte de triac
    """
    def __init__(self, numero, nb_ports = 8):
        Carte.__init__(self, numero, nb_ports)
        self.liste_triac = [ Triac(numero, i) for i in range(1,nb_ports+1)]


    def get_triac(self, indice_triac):
        return self.liste_triac[indice_triac-1]
