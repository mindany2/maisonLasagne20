from In_out.external_boards.relay.Relay import Relay
from In_out.network.messages.set.Set_relay import Set_relay

class Relay_network(Relay):
    """
    This relay is from another rpi on the network
    """
    def __init__(self, rpi, address):
        Relay.__init__(self)
        self.rpi = rpi
        self.address = address

    def reload(self):
        self.rpi.send(Set_relay(self.address, self.state))

    def __str__(self):
        return str(self.address)
