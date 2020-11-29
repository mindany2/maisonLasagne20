from tree.connected_objects.Lamp import Lamp
from tree.utils.Color import Color
from time import sleep
from random import randrange
from In_out.cartes.relais.Relais import Etat
from In_out.wifi_devices.Wifi_device import Wifi_device
from utils.Logger import Logger

class Led(Lamp):
    """
    RGB strip led
    """
    def __init__(self, name, relay, controler, color = 0):
        Lamp.__init__(self, name, relay)
        self.color = Color(color)
        self.dimmer = 0
        self.controler = controler

    def connect(self):
        if not(self.connected):
            Logger.info("Trying to connect to"+self.name)
            if self.color.is_black() and not(self.force):
                self.set_relay(Etat.ON)
                sleep(1)
            self.connected = not(self.controler.connect())
            if not(self.connected):
                # the led is out of order
                self.set_relay(Etat.OFF)
        return not(self.connected)

    def disconnect(self):
        if self.connected:
            sleep(0.5)
            self.controler.deconnect(is_black = self.color.is_black())
            if self.color.is_black() and not(self.force):
                self.set_relay(Etat.OFF)
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
            self.set_relay(Etat.ON)
            ko = self.controler.connect(attempts = 5)
            if ko:
                Logger.error("The led {} is out of order".format(self.name))
                for _ in range(0,3):
                    self.set_relay(Etat.OFF)
                    sleep(3)
                    self.set_relay(Etat.ON)
                    sleep(3)
                return True
            self.disconnect()
            self.set_relay(Etat.OFF)
        return False


