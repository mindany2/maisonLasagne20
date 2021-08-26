from In_out.zigbee.devices.Zigbee_device import Zigbee_device

class Zigbee_contact(Zigbee_device):
    """
    This is a door/windows contact
    """
    def __init__(self, name, device, interrupt):
        Zigbee_device.__init__(self, name, device, interrupt)

    def update(self, data):
        if isinstance(data["data"], str):
            super().update("1" in data["data"])

