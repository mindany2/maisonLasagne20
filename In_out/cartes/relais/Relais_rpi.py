from In_out.cartes.relais.Relais import Relais
from utils.communication.set.Set_relais import Set_relais

class Relais_rpi(Relais):
    """
    Ceci est un relais
    """
    def __init__(self, rpi, addresse):
        Relais.__init__(self)
        self.rpi = rpi
        self.addresse = addresse

    def reload(self):
        self.rpi.send(Set_relais(self.addresse, self.etat))
