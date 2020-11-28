from tree.connected_objects.Light import Light
from tree.utils.Color import Color
from time import sleep
from random import randrange
from In_out.cartes.relay.Relais import Etat
from In_out.wifi_devices.Wifi_device import Wifi_device
from utils.Logger import Logger

class Led(Light):
    """
    RGB strip led
    """
    def __init__(self, name, relay, controler, color = 0):
        Light.__init__(self, name)
        self.color = Color(color)
        self.dimmer = 0
        self.relay =  relay
        self.controler = controler
        self.connected = False
        self.force = False

    def force_relay(self, force):
        # force the relay always to ON
        self.force = force
        if force:
            self.relay.set(Etat.ON)
        elif not(self.connected):
            self.relay.set(Etat.OFF)

    def connect(self):
        if not(self.connected):
            Logger.info("Trying to connect to"+self.name)
            if self.color.is_black() and not(self.force):
                self.relay.set(Etat.ON)
                sleep(1)
            self.connected = not(self.controler.connect())
            if not(self.connected):
                # the led is out of order
                self.relay.set(Etat.OFF)
        return not(self.connected)

    def disconnect(self):
        if self.connected:
            sleep(0.5)
            self.controler.deconnect(is_black = self.color.is_black())
            if self.color.is_black() and not(self.force):
                self.relay.set(Etat.OFF)
            self.connected = False

    def set(self, dimmer, color):
        err1, err2 = 0,0
        if self.color != Color(color, dimmer):
            self.color = Color(color, dimmer)
            err1 = self.controler.send_color(self.color)
        if self.dimmer != dimmer:
            self.dimmer = dimmer
            err2 = self.controler.send_dimmer(self.dimmer)
        return (err1 or err2)

    def repair(self):
        if isinstance(self.controler, Wifi_device):
            Logger.info("Trying to connect to "+self.name)
            self.relay.set(Etat.ON)
            ko = self.controler.connect(attempts = 5)
            if ko:
                Logger.error("The led {} is out of order".format(self.name))
                for _ in range(0,3):
                    self.relay.set(Etat.OFF)
                    sleep(3)
                    self.relay.set(Etat.ON)
                    sleep(3)
                return True
            self.disconnect()
            self.relay.set(Etat.OFF)
        return False


