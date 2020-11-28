from tree.connected_objects.Lamp import Lamp
from enum import Enum

class Strombo(Lamp):
    """
    Small stromboscop : Fun Generation LED Pot Strobe 100
    https://www.thomann.de/intl/fun_generation_led_pot_strobe_100.htm
    """
    def __init__(self, name, relay, controler):
        Lamp.__init__(self, name, relay)
        self.dmx = controler

        self.dimmer = 0
        self.strombo = 0

    def set_dimmer(self, value):
        if self.dimmer != value:
            self.dmx.set(CHANNEL.dimmer, value)
        self.dimmer = value

    def set_strombo(self, value):
        if self.strombo != value:
            self.dmx.set(CHANNEL.strombo, value)
        self.strombo = value

    def lock_dimmer(self):
        super().lock()

    def unlock_dimmer(self):
        super().unlock()

class CHANNEL(Enum):
    dimmer = 1
    program = 2
    strombo = 3

