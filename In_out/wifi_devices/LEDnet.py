from In_out.utils.Magic_Home import MagicHomeApi
from In_out.wifi_devices.Wifi_device import Wifi_device
from time import sleep

class LEDnet(Wifi_device):
    """
    Wifi led controller
    https://tinyurl.com/magichomecontroller
    """
    def __init__(self, ip):
        Wifi_device.__init__(self, ip)
        self.controleur = MagicHomeApi(self.ip, 0)

    def connect(self, attempts = 20):
        for _ in range(0,attempts):
            err = self.controleur.connect()
            if not(err):
                # the led success to connect
                break
            sleep(0.5)
        return err

    def send_color(self, couleur):
        r,g,b = couleur.int_to_rgb()
        self.controleur.update_device(r,g,b,0)

    def send_dimmeur(self, dimmeur):
        # there are no dimmer in this led
        pass

    def disconnect(self, is_black=True):
        if is_black:
            self.controleur.disconnect()
        
