from data_manager.read_tree.reload_tree import reload_tree
from threading import Thread
from In_out.network.messages.Message import Message

class Reload_tree(Message):

    def __init__(self):
        pass

    def do(self, getter):
        reload_tree(getter)
        #Thread(target=reload_tree, args=[getter]).run()
