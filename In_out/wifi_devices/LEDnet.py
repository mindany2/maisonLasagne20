from In_out.utils.Magic_Home import MagicHomeApi
from In_out.wifi_devices.Wifi_device import Wifi_device

class LEDnet(Wifi_device):
    """
    type de controleur led wifi
    """
    def __init__(self, ip):
        Wifi_device.__init__(self, ip)
        self.controleur = MagicHomeApi(self.ip, 0)

    def connect(self):
        return self.controleur.connect()

    def send_color(self, couleur):
        r,g,b = couleur.int_to_rgb()
        self.controleur.update_device(r,g,b,0)

    def send_dimmeur(self, dimmeur):
        # on a pas de dimmeur sur ce controleur
        pass

    def deconnect(self, is_black=True):
        if is_black:
            self.controleur.deconnect()
        
