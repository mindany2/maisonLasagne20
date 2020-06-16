from In_out.utils.Bluetooth import Bluetooth
from In_out.bluetooth_devices.Bluetooth_device import Bluetooth_device

class TRIONES(Bluetooth_device):
    """
    Les controleur leds avec 1 seule branche et 5 pins 
    """
    def __init__(self, addr):
        Bluetooth_device.__init__(self,addr, 0xffd5, 0xffd9)

    def send_color(self, couleur):
        valeur = "0x56"+couleur.valeur[2::]+"00f0aa"
        self.send(valeur)

    def send_dimmeur(self, dimmeur):
        #ce controleur n'a pas de dimmeur,
        # on fait donc rien
        pass

