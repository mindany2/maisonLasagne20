from tree.connected_objects.dmx.Dmx_device import Dmx_device
from tree.utils.Color import Color
from time import sleep
from enum import Enum

class Dmx_strip_led(Dmx_device):
    """
    Strip led connected by dmx
    """
    def __init__(self, name, relay, addr, dmx, color = "0x000000"):
        Dmx_device.__init__(self, name, relay, addr, dmx)
        self.color = Color(color)
        self.dimmer = 0

    def connect(self):
        if self.color.is_black() and not(self.force):
            self.set_state(True)
        super().connect()
        return True

    def disconnect(self):
        if self.color.is_black() and not(self.force):
            self.set_state(False)
        super().disconnect()

    def set_color(self, dimmer, color):
        if self.color != Color(color):
            self.color = Color(color)
        if self.dimmer != dimmer:
            self.dimmer = dimmer
        rgb = self.color.dim(self.dimmer).int_to_rgb()
        for val,channel in zip(rgb, CHANNEL):
            super().set(channel, val)
            
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : led dmx\n")
        string += "".join("- Status : dimmer={} color={}\n".format(self.dimmer, self.color))
        string += "".join("- Controler : {}\n".format(super()))
        return string

class CHANNEL(Enum):
    red = 1
    green = 2
    blue = 3

