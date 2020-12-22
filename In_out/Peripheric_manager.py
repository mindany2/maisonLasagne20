class Peripheric_manager:
    """
    This is a class that store all the differents peripheric
    of the tree running process (so no interrupt)
    """

    def __init__(self):
        self.list_boards_relay = []
        self.dmx = None
        self.name = None
        self.port_extender = None
        self.spotify = None
        self.amps = {}
        self.st_nucleos = {}
        self.connections = {}

    def initialize(self):
        if self.spotify:
            self.spotify.initialize()
        for conn in self.connections.values():
            conn.initialize()

    # SET
    def set_name(self, name):
        self.name = name

    def set_connection(self, connection):
        self.connections[connection.name] = connection

    def set_dmx(self, dmx):
        self.dmx = dmx

    def set_st_nucleo(self, st_nucleo):
        self.st_nucleos[st_nucleo.name] = st_nucleo

    def set_amp(self, amp):
        self.amps[amp.name] = amp

    def set_spotify(self, spotify):
        self.spotify = spotify

    def set_extender(self, extender):
        self.port_extender = extender

    def set_relay_board(self, board):
        self.list_boards_relay.append(board)

    # GET 

    def get_name(self):
        return self.name

    def get_connection(self, name):
        conn = self.connections[name]
        if conn: return conn
        raise(NameError("The connection to {} is not configured".format(name)))

    def get_dmx(self):
        if self.dmx: return self.dmx
        raise(NameError("There are no dmx network configured"))

    def get_st_nucleo(self, name):
        st_nucleo = self.st_nucleos[name]
        if st_nucleo: return st_nucleo
        raise(NameError("There are no st_nucleos name {} configured".format(name)))

    def get_amp(self, name):
        try:
            amp = self.amps[name]
            if amp: return amp
        except KeyError:
            raise(NameError("There are no amp name {} configured".format(name)))

    def get_spotify(self):
        if self.spotify: return self.spotify
        raise(NameError("There are no spotify configured"))

    def get_extender(self):
        if self.port_extender: return self.port_extender
        raise(NameError("There are no port_extender configured"))

    def get_relay(self, index_board, index_relay):
        if index_board < 1:
            raise(IndexError("Invalid index board {}, it starts from 1".format(index_board)))
        board = self.list_boards_relay[index_board-1]
        if board: 
            relay = board.get_relay(index_relay)
            if relay: return relay
            raise(IndexError("There are no relay number {} in th board index {}".format(index_relay, index_board)))
        raise(IndexError("There are no board with the index {} configured".format(index_board)))

    def get_triak(self, index_board, index_triak):
        # search witch st is it
        for st in self.st_nucleos.values():
            board = st.get_board_triak(index_board)
            if board: 
                triak = board.get_triak(index_triak)
                if triak: return triak
                raise(IndexError("There are no relay number {} in the board index {} ".format(index_triak, index_board)))
        raise(IndexError("There are no board with the index {}".format(index_board)))

    def __str__(self):
        string  = "---- Peripheric manager ----\n"
        string += "Relay boards : {}\n".format(self.list_boards_relay)
        string += "Dmx : {}\n".format(self.dmx)
        string += "Port_extender : {}\n".format(self.port_extender)
        string += "Spotify : {}\n".format(self.spotify)
        string += "Amps : {}\n".format(self.amps)
        string += "ST_nucleos :\n"
        string += "".join(["|-{}\n".format(string) for string in self.st_nucleos.values()])
        string += "".join("Connections : {}\n".format(self.connections))
        return string


