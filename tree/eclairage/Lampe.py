from tree.eclairage.Lumiere import Lumiere
from time import sleep

from utils.In_out.controle.Relais import Relais, Etat

class Lampe(Lumiere):
    """
    led en bluetooth
    """
    def __init__(self, nom, relais):
        Lumiere.__init__(self, nom)
        self.relais =  relais

    def set(self, on_off):
        if on_off:
            etat = Etat.ON
        else:
            etat = Etat.OFF
        self.relais.set(etat)

    def show(self):
        self.relais.show()

