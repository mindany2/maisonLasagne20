from In_out.dmx.controllers.Dmx_controller import Dmx_controller
from In_out.network.communication.set.Set_DMX import Set_DMX

class Dmx_network(Dmx_controller):
    """
    send dmx order to a rpi through the network
    """
    def __init__(self, rpi):
        Dmx_controller.__init__(self)
        self.rpi = rpi

    def set(self, channel, value):
        super().set(channel, value)
        self.rpi.send(Set_DMX(channel, value))

