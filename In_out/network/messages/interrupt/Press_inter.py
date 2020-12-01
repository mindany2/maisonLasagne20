from tree.Tree import Tree
from In_out.network.messages.Message import Message

class Press_inter(Message):

    def __init__(self, name, state):
        self.name= name
        self.state = state

    def do(self):
        Tree().press_inter(self.name, self.state)
