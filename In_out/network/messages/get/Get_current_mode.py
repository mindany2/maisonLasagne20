from tree.Tree import Tree
from In_out.network.messages.Message import Message

class Get_current_mode(Message):

    def __init__(self):
        pass

    def do(self):
        return Tree().get_current_mode()
