from In_out.dmx.controllers.Dmx_controller import Dmx_controller
from In_out.network.messages.set.Set_DMX import Set_DMX

class Dmx_network(Dmx_controller):
    """
    send dmx order to a rpi through the network
    """
    def __init__(self, rpi, transmitters = []):
        Dmx_controller.__init__(self, transmitters)
        self.rpi = rpi

    def set(self, channel, value):
        super().set(channel, value)
        self.rpi.send(Set_DMX(channel, value))

    def connect(self, channel):
        return self.rpi.send(Set_DMX(channel, -1))

    def disconnect(self, channel):
        print(f"disconnect {channel}")
        return self.rpi.send(Set_DMX(channel, -2))

