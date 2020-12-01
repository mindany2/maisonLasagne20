
class Wifi_device:
    """
    Wifi device with ip and controler
    """

    def __init__(self, ip):
        self.ip = ip
        self.controler = None
