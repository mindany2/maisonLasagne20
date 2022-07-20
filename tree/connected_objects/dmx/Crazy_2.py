from tree.connected_objects.dmx.Dmx_device import Dmx_device
from enum import Enum

class Crazy_2(Dmx_device):
    """
    NICOLS Crazy II Led : Bowl that creat dots
    http://www.amplitude.fr/eclairage/location-particuliers-effets-automatiques/nicols-crazy-ii-led
    """
    def __init__(self, name, relay, addr, dmx):
        Dmx_device.__init__(self, name, relay, addr, dmx)
        self.program = 0
        self.strombo = 0
        self.speed = 0

    def set_program(self, value):
        if self.program != value:
            super().set(CHANNEL.program, value)
        self.program = value

    def set_strombo(self, value):
        if self.strombo != value:
            super().set(CHANNEL.strombo, value)
        self.strombo = value

    def set_speed(self, value):
        if self.speed != value:
            super().set(CHANNEL.speed, value)
        self.speed = value

    def reload(self, other):
        if isinstance(other, Crazy_2):
            super().reload(other)
            self.program = other.program
            self.strombo = other.strombo
            self.speed = other.speed

    def __eq__(self, other):
        if isinstance(other, Crazy_2):
            return super().__eq__(other)\
                    and self.program == other.program\
                    and self.strombo == other.strombo\
                    and self.speed == other.speed
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Crazy_2\n")
        string += "".join("- Dmx : {}\n".format(super()))
        return string


class CHANNEL(Enum):
    program = 1
    speed = 2
    strombo = 3


