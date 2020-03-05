from commande.Triac import Triac
from commande.Carte import Carte
from commande.Bus import Bus

class Carte_triac(Carte):
    """
    Une carte de triac
    """
    def __init__(self, numero, port_bus, registre = 0x12, nb_ports = 8):
        Carte.__init__(self, numero, port_bus, registre, nb_ports)
        self.liste_triac = [ Triac(port_bus, registre, i) for i in range(1,nb_ports+1)]
        for i,pin in enumerate(Bus().read(port_bus, registre)):
            self.liste_triac[i].etat = pin


    def get_triac(self, indice_triac):
        return self.liste_triac[indice_triac-1]
