from In_out.network.messages.Message import Message

class Network_interrupt(Message):

    def __init__(self, name, name_inter, state):
        self.name = name
        self.name_inter = name_inter
        self.state = state

    def do(self, getter):
        getter.get_manager().get_connection(self.name).press_inter(self.name_inter)
