from tree.Tree import Tree
from In_out.network.messages.Message import Message

class Reload_html(Message):

    def __init__(self):
        pass

    def do(self):
        Tree().reload_html()
