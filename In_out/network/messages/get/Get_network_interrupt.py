from In_out.network.messages.Message import Message

class Get_network_interrupt(Message):

    def __init__(self, name):
        self.name = name

    def do(self, getter):
        return getter.get_manager().get_connection(self.name).get_input_interrupts()
