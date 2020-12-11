from tree.Tree import Tree
from In_out.network.messages.Message import Message

class Press_inter(Message):

    def __init__(self, name_env, name_bt, state):
        self.name_env = name_env
        self.name_bt = name_bt
        self.state = state

    def do(self, getter):
        getter.get_tree().press_inter(self.name_env, self.name_bt, not(self.state))
