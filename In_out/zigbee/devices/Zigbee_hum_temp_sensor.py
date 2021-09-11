from In_out.zigbee.devices.Zigbee_device import Zigbee_device

class Zigbee_hum_temp_sensor(Zigbee_device):
    """
    This is a door/windows contact
    """
    def __init__(self, name, device, interrupt):
        Zigbee_device.__init__(self, name, device, interrupt)
        self.humidity, self.temperature = None, None

    def update(self, data):
        if data["name"] == "temperature":
            self.temperature = data["value"]
        elif data["name"] == "humidity":
            self.humidity = data["value"]
        super().update((self.temperature, self.humidity))

