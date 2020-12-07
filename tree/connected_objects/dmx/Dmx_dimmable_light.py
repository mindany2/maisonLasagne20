from tree.connected_objects.Lamp import Lamp
from time import sleep
from enum import Enum

class Dmx_dimmable_light(Lamp):
    """
    Simple dimmer light in dmx
    """
    def __init__(self, nom, relay, controler):
        Lamp.__init__(self, nom, relay)
        self.dmx = controler
        self.dimmer = 0

    def set_dimmer(self, value):
        if self.dimmer != value:
            self.dmx.set(CHANNEL.dimmer, value)
        self.dimmer = value

    def set(self, on_off):
        super().set(on_off)
        # TODO
        """
        if value == True:
            # need to wait before the light is initialise
            sleep(4)
        """

    def lock_dimmer(self):
        super().lock()
        if self.dimmer == 0:
            self.set(1)

    def test_dimmer(self):
        return super().test()

    def unlock_dimmer(self):
        super().unlock()
        if self.dimmer == 0:
            self.set(0)

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Dmx_dimmable_light\n")
        string += "".join("- Dmx : {}\n".format(self.dmx))
        return string



class CHANNEL(Enum):
    dimmer = 1

