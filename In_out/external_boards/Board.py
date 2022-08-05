
class Board:
    """
    Une board de relay
    """
    def __init__(self, number, port_bus, nb_ports = 8):
        self.number = number
        self.port_bus = port_bus
        self.nb_ports = nb_ports

    def get_number(self):
        return self.number

    def change_number(self, number):
        self.number = number

    def __str__(self):
        return "Number : {}".format(self.number)
