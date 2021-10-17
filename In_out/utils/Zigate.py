import zigate

class Zigate:
    """
    Manage the zigbee interface with zigate
    """
    def __init__(self, send):
        self.send = send
        self.zigbee = zigate.connect(port=None)
        zigate.dispatcher.connect(self.call_back, zigate.dispatcher.Any)

    def get_devices(self):
        return self.zigbee.devices

    def call_back(self, signal, sender, **kwargs):
        if signal == zigate.ZIGATE_ATTRIBUTE_UPDATED:
            self.send(kwargs["device"], kwargs["attribute"])

    def permit_join(self):
        self.zigbee.permit_join()

if __name__ == "__main__":
    z = Zigate(lambda device, attr : print(device, attr))
    print("connected")
    z.permit_join()
    while True:
        pass


