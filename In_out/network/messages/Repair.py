from tree.Tree import Tree
from In_out.network.messages.Message import Message

class Repair(Message):

    def __init__(self):
        Message.__init__(self)

    def do(self, getter):
        getter.get_tree().repair()
