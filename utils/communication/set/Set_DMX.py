from In_out.Gestionnaire_peripheriques import Gestionnaire_peripheriques
from utils.communication.Message import Message

class Set_DMX(Message):

    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def do(self):
        Gestionnaire_peripheriques().get_dmx().set(self.addr, self.value)
