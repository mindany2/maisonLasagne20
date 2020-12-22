from In_out.network.messages.Message import Message

class Network_interrupt(Message):

    def __init__(self, ip, name_inter, state):
        self.ip = ip
        self.name_inter = name_inter
        self.state = state

    def do(self, getter):
        getter.get_manager().get_connection_by_ip(self.ip).press_inter(self.name_inter)
