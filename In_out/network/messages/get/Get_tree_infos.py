from In_out.network.messages.Message import Message

class Get_tree_infos(Message):

    def __init__(self):
        pass

    def do(self, getter):
        return str(getter.get_tree())
