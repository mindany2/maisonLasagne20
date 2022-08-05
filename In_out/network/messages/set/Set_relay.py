from In_out.network.messages.Message import Message

class Set_relay(Message):

    def __init__(self, addr, value):
        self.addr = addr
        self.value = value

    def do(self, getter):
        getter.get_manager().get_relay(self.addr[0], self.addr[1]).set(self.value)
