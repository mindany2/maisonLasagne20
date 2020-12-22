from In_out.network.Connection import Connection

class Rpi(Connection):
    """
    Distant Rpi
    """
    def __init__(self, name, addr, me):
        Connection.__init__(self, name, addr, me)



