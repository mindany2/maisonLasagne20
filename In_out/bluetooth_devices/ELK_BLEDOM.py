from In_out.utils.Bluetooth import Bluetooth
from In_out.bluetooth_devices.Bluetooth_device import Bluetooth_device

class ELK_BLEDOM(Bluetooth_device):
    """
    Led strip controller RGB
    https://tinyurl.com/elkbledom
    this was reverse engineering
    """
    def __init__(self, addr):
        Bluetooth_device.__init__(self,addr, 0xfff0, 0xfff3)

    def send_dimmer(self, dimmer):
        dimmer = int(250*float(dimmer)/100)
        value = "0x7e0401"+(dimmer < 16)*"0"+hex(dimmer)[2::]+"01ffff00ef"
        return self.send(value)

    def send_color(self, color):
        value = "0x7e070503"+color.value[2::]+"10ef"
        return self.send(value)
