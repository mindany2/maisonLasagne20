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
        self.controler = MagicHomeApi(self.ip, 0)

    def connect(self, attempts = 20):
        for _ in range(0,attempts):
            success = self.controler.connect()
            if success:
                # the led success to connect
                break
            sleep(0.5)
        return success

    def send_color(self, color):
        r,g,b = color.int_to_rgb()
        self.controler.update_device(r,g,b,0)

    def send_dimmer(self, dimmer):
        # there are no dimmer in this led
        pass

    def disconnect(self, is_black=True):
        if is_black:
            self.controler.disconnect()
        # time to make sure the led received the order
        sleep(5)
        
