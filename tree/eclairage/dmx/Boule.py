from tree.eclairage.Lampe import Lampe
from enum import Enum

class Boule(Lampe):
    """
    Boule centrale avec les petits points
    il y a 42 program
    """
    def __init__(self, nom, relais, controleur):
        Lampe.__init__(self, nom, relais)
        self.dmx = controleur

        self.program = 0
        self.strombo = 0
        self.vitesse = 0

    def set_program(self, value):
        if self.program != value:
            self.dmx.set(CHANNEL.program, value)
        self.program = value

    def set_strombo(self, value):
        if self.strombo != value:
            self.dmx.set(CHANNEL.strombo, value)
        self.strombo = value

    def set_vitesse(self, value):
        if self.vitesse != value:
            self.dmx.set(CHANNEL.vitesse, value)
        self.vitesse = value

class CHANNEL(Enum):
    program = 1
    vitesse = 2
    strombo = 3


