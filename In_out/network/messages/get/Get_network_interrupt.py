from In_out.network.messages.Message import Message

class Get_network_interrupt(Message):

    def __init__(self, ip):
        self.ip = ip

    def do(self, getter):
        return getter.get_manager().get_connection_by_ip(self.ip).get_input_interrupts()
