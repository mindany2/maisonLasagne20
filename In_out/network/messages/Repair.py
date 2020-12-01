from tree.Tree import Tree
from In_out.network.messages.Message import Message

class Repair(Message):

    def __init__(self):
        pass

    def do(self):
        Tree().repair()
