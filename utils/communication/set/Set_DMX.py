from In_out.cartes.Gestionnaire_de_cartes import Gestionnaire_de_cartes
from utils.communication.Message import Message

class Set_DMX(Message):

    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def do(self):
        Gestionnaire_de_cartes().get_dmx().set(self.addr, self.value)
