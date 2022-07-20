from In_out.network.messages.Message import Message

class Change_mode(Message):

    def __init__(self, nv_mode):
        self.nv_mode = nv_mode

    def do(self, getter):
        getter.get_tree().change_mode(self.nv_mode)
