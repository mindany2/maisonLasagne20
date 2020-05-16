
class Carte:
    """
    Une carte de relais
    """
    def __init__(self, numero, port_bus, nb_ports = 8):
        self.numero = numero
        self.port_bus = port_bus
        self.nb_ports = nb_ports
