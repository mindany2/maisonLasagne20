from In_out.dmx.controleurs.Controleur_dmx import Controleur_dmx
from utils.communication.set.Set_DMX import Set_DMX
from utils.communication.Client import Client
from utils.Logger import Logger

class RpiDMX(Controleur_dmx):
    """
    Envoi les informations dmx a un rpi qui est connecté
    à un réseau DMX
    """
    def __init__(self, addr):
        Controleur_dmx.__init__(self, addr)

    def set(self, channel, value):
        client = Client(self.addr)
        client.send(Set_DMX(channel, value))

