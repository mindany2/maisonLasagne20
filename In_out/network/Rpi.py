from In_out.network.Connection import Connection

class Rpi(Connection):
    """
    Distant Rpi
    """
    def __init__(self, name, addr):
        Connection.__init__(self, name, addr)



