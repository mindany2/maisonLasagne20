from tree.scenario.Instruction_enceinte import Instruction_enceinte
from tree.eclairage.Lumiere import Lumiere
from threading import Thread, Lock
from tree.scenario.Scenario import MARQUEUR

class Enceintes(Lumiere):
    """
    Gère une paire d'enceinte
    ( lier a une zone )
    """

    def __init__(self, nom, ampli, zone):
        Lumiere.__init__(self, nom)
        self.ampli = ampli
        self.zone = zone
        self.connected = False

    def volume(self):
        return self.zone.volume

    def connect(self):
        if not(self.connected) and self.volume() == 0:
            self.ampli.allumer()
            self.connected = True

    def deconnect(self):
        if self.connected and self.volume() == 0:
            self.ampli.eteindre()
            self.connected = False

    def change_volume(self, valeur):
        if valeur == 0:
            self.zone.set_power(0)
        elif valeur != 0 and self.zone.power == 0:
            self.zone.set_power(1)
        self.zone.set_volume(valeur)

    def show(self):
        print("Enceinte " + str(self.zone.numero))

