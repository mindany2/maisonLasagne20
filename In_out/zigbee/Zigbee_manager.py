from In_out.utils.Zigate import Zigate
from In_out.zigbee.devices.Zigbee_device import Zigbee_device
from tree.utils.List import List
from tree.utils.Logger import Logger
import re


class Zigbee_manager:
    """
    Manage all the zigbee devices
    """
    def __init__(self, constructor = Zigate):
        """
        :param constructor: the type of the constructor"""

        self.zigbee = constructor(self.interrupt)
        self.devices_tab = {}
        for device in self.zigbee.get_devices():
            match = re.match(r'[\(]*\((?P<addr>([^\)]*))', str(device.addr))
            if match:
                addr = match.group("addr")
            else:
                addr = device.addr
            self.devices_tab[addr.strip()] = device

        Logger.info(f"All zigbee devices :\n{self}")

        self.know_devices = {}

    def add_device(self, device):
        self.know_devices[device.get_device()] = device 

    def get_device(self, addr):
        try:
            return self.devices_tab[addr]
        except KeyError:
            return None

    def interrupt(self, device, data):
        if device in self.know_devices:
            self.know_devices[device].update(data)

    def __str__(self):
        return "\n".join(f"{addr} :  {device}" for addr, device in self.devices_tab.items())


if __name__ == "__main__":
    z = Zigbee_manager()
    while True:
        pass
