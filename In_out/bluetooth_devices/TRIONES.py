from In_out.utils.Bluetooth import Bluetooth
from In_out.bluetooth_devices.Bluetooth_device import Bluetooth_device

class TRIONES(Bluetooth_device):
    """
    Led strip controller RGB
    https://tinyurl.com/triones
    this was reverse engineering 
    """
    def __init__(self, addr):
        Bluetooth_device.__init__(self,addr, 0xffd5, 0xffd9)

    def send_color(self, color):
        value = "0x56"+color.value[2::]+"00f0aa"
        self.send(value)

    def send_dimmer(self, dimmer):
        # this led have not any dimmer
        pass

