class Peripheric_manager:
    """
    This is a static class that store all the differents peripheric
    of the tree running process (so no interrupt)
    """
    list_boards_relay = []
    list_boards_triak = []
    dmx = None
    port_extender = None
    spotify = None
    amps = {}
    st_nucleos = {}
    connections = {}

    # SET

    @classmethod
    def set_connection(self, connection):
        self.connections[connection.name] = connection

    @classmethod
    def set_dmx(self, dmx):
        self.dmx = dmx

    @classmethod
    def set_st_nucleo(self, st_nucleo):
        self.st_nucleos[st_nucleo.name] = st_nucleo

    @classmethod
    def set_amp(self, amp):
        self.amps[amp.name] = amp

    @classmethod
    def set_spotify(self, spotify):
        self.spotify = spotify

    @classmethod
    def set_extender(self, extender):
        self.port_extender = extender

    @classmethod
    def set_relay_board(self, board):
        self.list_boards_relay.append(board)

    @classmethod
    def set_triak_board(self, board):
        self.list_boards_triak.append(board)

    # GET 

    @classmethod
    def get_connections(self, name):
        return self.connections[name]

    @classmethod
    def get_dmx(self):
        return self.dmx

    @classmethod
    def get_st_nucleo(self, name):
        return self.st_nucleos[name]

    @classmethod
    def get_amp(self, name):
        return self.amps[name]

    @classmethod
    def get_spotify(self):
        return self.spotify

    @classmethod
    def get_extender(self):
        return self.port_extender

    @classmethod
    def get_relay(self, indice_carte, indice_relay):
        return self.list_carte_relay[indice_carte-1].get_relay(indice_relay)

    @classmethod
    def get_triak(self, indice_carte, indice_triak):
        return self.list_carte_triak[indice_carte-1].get_triak(indice_triak)


