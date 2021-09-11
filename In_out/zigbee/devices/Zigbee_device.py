
class Zigbee_device:
    """
    This is a simple zigbee device
    """
    def __init__(self, name, device, interrupt):
        self.device, self.name = device, name
        self.data = None
        self.interrupt = interrupt

    def get_device(self):
        return self.device

    def update(self, data):
        self.data = data
        self.interrupt.press(data)
