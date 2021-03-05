from tree.connected_objects.Lamp import Lamp
from tree.utils.Color import Color
from time import sleep
from random import randrange
from In_out.external_boards.relay.Relay import STATE
from In_out.wifi_devices.Wifi_device import Wifi_device
from tree.utils.Logger import Logger

class Led(Lamp):
    """
    RGB strip led
    """
    def __init__(self, name, relay, controler, color = "0x000000"):
        Lamp.__init__(self, name, relay)
        self.color = Color(color)
        self.controler = controler
        self.dimmer = 0

    def connect(self):
        if not(self.connected):
            if self.color.is_black() and not(self.force):
                self.set_state(True)
                sleep(1)
            self.connected = self.controler.connect()
            if not(self.connected):
                # the led is out of order
                Logger.error("The led {} is out of order".format(self.name))
                self.set_state(False)
            else:
                Logger.info("Connected to {}".format(self.name))
                # only one type of led have a real dimmer,
                # but need to be up
                self.controler.send_dimmer(100)
        return self.connected

    def disconnect(self):
        if self.connected:
            sleep(0.5)
            self.controler.disconnect(is_black = self.color.is_black())
            if self.color.is_black() and not(self.force):
                self.set_state(False)
            self.connected = False

    def set_color(self, dimmer, color):
        if self.color != Color(color):
            self.color = Color(color)

        if self.dimmer != dimmer:
            self.dimmer = dimmer
        return self.controler.send_color(self.color.dim(self.dimmer))

    def repair(self):
        if isinstance(self.controler, Wifi_device):
            Logger.info("Trying to connect to "+self.name)
            self.set_state(STATE.ON)
            ko = self.controler.connect(attempts = 5)
            if ko:
                Logger.error("The led {} is out of order".format(self.name))
                for _ in range(0,3):
                    self.set_state(STATE.OFF)
                    sleep(3)
                    self.set_state(STATE.ON)
                    sleep(3)
                return True
            self.disconnect()
            self.set_state(STATE.OFF)
        return False

    def reload(self, other):
        if isinstance(other, Led):
            self.dimmer == other.dimmer
            self.color = other.color

    def __eq__(self, other):
        if isinstance(other, Led):
            return super().__eq__(other)\
                    and self.relay == other.relay\
                    and self.dimmer == other.dimmer\
                    and self.color == other.color\
                    and self.controler == other.controler
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : led\n")
        string += "".join("- Status : dimmer={} color={}\n".format(self.dimmer, self.color))
        string += "".join("- Controler : {}\n".format(self.controler))
        return string


