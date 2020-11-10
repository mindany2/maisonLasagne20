from tree.eclairage.Lampe import Lampe
from time import sleep
from enum import Enum

class Decoupe(Lampe):
    """
    Decoupe étage
    """
    def __init__(self, nom, relais, controleur):
        Lampe.__init__(self, nom, relais)
        self.dmx = controleur
        self.dimmeur = 0

    def set_dimmeur(self, value):
        if self.dimmeur != value:
            self.dmx.set(CHANNEL.dimmeur, value)
        self.dimmeur = value

    def set(self, value):
        super().set(value)
        if value == True:
            # on doit attendre que le projo s'initialise
            sleep(4)


    def lock_dimmeur(self):
        super().lock()

    def test_dimmeur(self):
        return super().test()

    def unlock_dimmer(self):
        super().unlock()

class CHANNEL(Enum):
    dimmeur = 1

