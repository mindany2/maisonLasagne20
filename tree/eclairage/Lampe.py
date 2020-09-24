from tree.eclairage.Lumiere import Lumiere
from time import sleep
from threading import Lock
from In_out.cartes.relais.Relais import Etat
from utils.Logger import Logger

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
        Logger.info("on met la lampe {} a {}".format(self.nom, etat))
        if self.relais.etat != etat:
            self.relais.set(etat)

    def etat(self):
        return self.relais.etat

    def show(self):
        self.relais.show()

