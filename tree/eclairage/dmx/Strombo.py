from tree.eclairage.Lumiere import Lumiere
from enum import Enum

class Strombo(Lumiere):
    """
    Petit strombo
    """
    def __init__(self, nom, controleur):
        Lumiere.__init__(self, nom)
        self.dmx = controleur

        self.dimmeur = 0
        self.strombo = 0

    def set_dimmeur(self, value):
        if self.dimmeur != value:
            self.dmx.set(CHANNEL.dimmeur, value)
        self.dimmeur = value

    def set_strombo(self, value):
        if self.strombo != value:
            self.dmx.set(CHANNEL.strombo, value)
        self.strombo = value

    def lock_dimmeur(self):
        super().lock()

    def unlock_dimmer(self):
        super().unlock()

class CHANNEL(Enum):
    dimmeur = 1
    program = 2
    strombo = 3

