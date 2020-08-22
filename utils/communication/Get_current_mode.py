from tree.Tree import Tree
from utils.communication.Message import Message

class Get_current_mode(Message):

    def __init__(self):
        pass

    def do(self):
        return Tree().get_current_mode()
