from tree.connected_objects.Led import Led
from tree.utils.Color import Color
from time import sleep
from enum import Enum

class Dmx_strip_led(Led):
    """
    Strip led connected by dmx
    """
    def __init__(self, name, relay, controler):
        Led.__init__(self, name, relay, None)
        self.dmx = controler

    def connect(self):
        return True

    def disconnect(self):
        return True

    def set_color(self, dimmer, color):
        if self.color != Color(color):
            self.color = Color(color)
        if self.dimmer != dimmer:
            self.dimmer = dimmer
        rgb = self.color.dim(self.dimmer).int_to_rgb()
        for val,channel in zip(rgb, CHANNEL):
            self.dmx.set(channel, val)
            
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : led dmx\n")
        string += "".join("- Status : dimmer={} color={}\n".format(self.dimmer, self.color))
        string += "".join("- Controler : {}\n".format(self.dmx))
        return string

class CHANNEL(Enum):
    red = 1
    green = 2
    blue = 3

