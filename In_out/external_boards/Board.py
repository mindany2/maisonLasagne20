
class Board:
    """
    Une board de relay
    """
    def __init__(self, number, port_bus, nb_ports = 8):
        self.number = number
        self.port_bus = port_bus
        self.nb_ports = nb_ports
