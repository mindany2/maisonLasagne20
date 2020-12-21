from In_out.utils.Port_extender import Port_extender
from In_out.external_boards.relay.Relay import Relay

class Relay_port_extender(Relay):
    """
    It is a relay from the port extender pins
    """
    def __init__(self, extender, port_bus, registre, number):
        Relay.__init__(self)
        self.port_bus = port_bus
        self.number = number
        self.registre = registre
        self.bus = extender

    def reload(self):
        self.bus.write_pin(self.port_bus, self.registre, self.number, self.state.value)

    def __str__(self):
        return str(self.number)
