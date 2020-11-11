from In_out.Gestionnaire_peripheriques import Gestionnaire_peripheriques
from utils.communication.Message import Message

class Set_relais(Message):

    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def do(self):
        Gestionnaire_peripheriques().get_relais(self.addr[0], self.addr[1]).set(self.value)
