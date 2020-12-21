from In_out.external_boards.Board import Board

class Board_relay(Board):
    """
    A relay board like :
    https://tinyurl.com/16relayboard
    """
    def __init__(self, number, port_bus, nb_ports = 16):
        Board.__init__(self, number, port_bus, nb_ports)
        self.list_relay = []

    def get_relay(self, index_relay):
        if index_relay-1 < len(self.list_relay):
            return self.list_relay[index_relay-1]
        return None
        


