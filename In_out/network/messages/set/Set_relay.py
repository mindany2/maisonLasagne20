from In_out.Peripheric_manager import Peripheric_manager
from In_out.network.messages.Message import Message

class Set_relais(Message):

    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def do(self):
        Peripheric_manager().get_relais(self.addr[0], self.addr[1]).set(self.value)
