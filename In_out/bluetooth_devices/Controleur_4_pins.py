from In_out.utils.Bluetooth import Bluetooth
from In_out.bluetooth_devices.Bluetooth_device import Bluetooth_device

class Controleur_4_pins(Bluetooth_device):
    """
    Les controleur leds avec 2 branches et 4 pins 
    """
    def __init__(self, addr):
        Bluetooth_device.__init__(self,addr, 0xfff0, 0xfff3)

    def send_dimmeur(self, dimmeur):
        dimmeur = int(250*float(dimmeur)/100)
        valeur = "0x7e0401"+(dimmeur < 16)*"0"+hex(dimmeur)[2::]+"01ffff00ef"
        self.send(valeur)

    def send_color(self, couleur_hex):
        valeur = "0x7e070503"+couleur_hex[2::]+"10ef"
        self.send(valeur)
