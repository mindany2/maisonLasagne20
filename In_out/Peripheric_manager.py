class Peripheric_manager:
    """
    This is a static class that store all the differents peripheric
    of the tree running process (so no interrupt)
    """
    list_boards_relay = []
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

    # GET 

    @classmethod
    def get_connections(self, name):
        conn = self.connections[name]
        if conn: return conn
        raise(NameError("The connection to {} is not configured".format(name)))

    @classmethod
    def get_dmx(self):
        if self.dmx: return self.dmx
        raise(NameError("There are no dmx network configured"))

    @classmethod
    def get_st_nucleo(self, name):
        st_nucleo = self.st_nucleos[name]
        if st_nucleo: return st_nucleo
        raise(NameError("There are no st_nucleos name {} configured".format(name)))

    @classmethod
    def get_amp(self, name):
        amp = self.amps[name]
        if amp: return amp
        raise(NameError("There are no st_nucleos name {} configured".format(name)))

    @classmethod
    def get_spotify(self):
        if self.spotify: return self.spotify
        raise(NameError("There are no spotify configured"))

    @classmethod
    def get_extender(self):
        if self.port_extender: return self.port_extender
        raise(NameError("There are no port_extender configured"))

    @classmethod
    def get_relay(self, index_board, index_relay):
        board = self.list_boards_relay[index_board-1]
        if board: 
            relay = board.get_relay(index_relay)
            if relay: return relay
            raise(IndexError("There are no relay number {} in th board index {}".format(index_relay, index_board)))
        raise(IndexError("There are no board with the index {} configured".format(index_board)))

    @classmethod
    def get_triak(self, index_board, index_triak):
        # search witch st is it
        for st in self.st_nucleos:
            board = st.get_board_triak(index_board)
            if board:
                break
            else:
                index_board -= st.nb_boards()
        if board: 
            triak = board.get_relay(index_triak)
            if triak: return triak
            raise(IndexError("There are no relay number {} in the board index {} ".format(index_triak, index_board)))
        raise(IndexError("There are no board with the index {}".format(index_board)))
