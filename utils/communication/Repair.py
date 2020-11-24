from tree.Tree import Tree
from utils.communication.Message import Message

class Repair(Message):

    def __init__(self):
        pass

    def do(self):
        Tree().repair()
