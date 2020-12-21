from In_out.utils.Port_extender import Port_extender
from In_out.external_boards.relay.Board_relay import Board_relay
from In_out.external_boards.relay.Relay_port_extender import Relay_port_extender

class Board_relay_extender(Board_relay):
    """
    The board is link with the port extender
    """
    def __init__(self, extender, number, port_bus, nb_ports = 16):
        Board_relay.__init__(self, number, port_bus, nb_ports)
        self.list_relay = [ Relay_port_extender(extender, port_bus, 0x13*(i<8)+0x12*(i>7), i%8+1) for i in range(0,nb_ports)]
        """
        for i,pin in enumerate(Port_extender().read(port_bus, registre)):
            self.list_relay[i].state = pin
        """
        self.bus = extender
        self.bus.write(port_bus, 0x12, 0xff)
        self.bus.write(port_bus, 0x13, 0xff)
        self.bus.write(port_bus, 0x01, 0x0)
        self.bus.write(port_bus, 0x00, 0x0)

        # put the resistors
        self.bus.write(port_bus, 0x0d, 0xff)
        self.bus.write(port_bus, 0x0c, 0xff)



