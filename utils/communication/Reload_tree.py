from utils.Data_change.Create_tree import reload_tree
from utils.communication.Message import Message

class Reload_tree(Message):

    def __init__(self):
        pass

    def do(self):
        reload_tree()
