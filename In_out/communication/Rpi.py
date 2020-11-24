from In_out.communication.Connection import Connection

class Rpi(Connection):
    """
    Stocke les informations du rpi distant
    """
    def __init__(self, nom, addr):
        Connection.__init__(self, nom, addr)



