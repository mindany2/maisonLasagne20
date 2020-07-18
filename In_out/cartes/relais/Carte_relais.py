from In_out.cartes.Carte import Carte

class Carte_relais(Carte):
    """
    Une carte de relais de base
    """
    def __init__(self, numero, port_bus, nb_ports = 16):
        Carte.__init__(self, numero, port_bus, nb_ports)
        self.liste_relais = []

    def get_relais(self, indice_relais):
        return self.liste_relais[indice_relais-1]
        


