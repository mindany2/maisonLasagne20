from tree.connected_objects.Lamp import Lamp
from enum import Enum

class Crazy_2(Lamp):
    """
    NICOLS Crazy II Led : Bowl that creat dots
    http://www.amplitude.fr/eclairage/location-particuliers-effets-automatiques/nicols-crazy-ii-led
    """
    def __init__(self, name, relay, controler):
        Lamp.__init__(self, name, relay)
        self.dmx = controler

        self.program = 0
        self.strombo = 0
        self.speed = 0

    def set_program(self, value):
        if self.program != value:
            self.dmx.set(CHANNEL.program, value)
        self.program = value

    def set_strombo(self, value):
        if self.strombo != value:
            self.dmx.set(CHANNEL.strombo, value)
        self.strombo = value

    def set_speed(self, value):
        if self.speed != value:
            self.dmx.set(CHANNEL.speed, value)
        self.speed = value

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Crazy_2\n")
        string += "".join("- Dmx : {}\n".format(self.dmx))
        return string


class CHANNEL(Enum):
    program = 1
    speed = 2
    strombo = 3


