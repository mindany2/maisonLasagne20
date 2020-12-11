from In_out.network.messages.interrupt.Press_inter import Press_inter
from tree.Tree import Tree
from time import time

class Interrupt:
    """
    This is an interrupt for the interrupt process
    that send it's value to the tree process
    """

    def __init__(self, name, client):
        self.name = name
        self.client = client

    def press(self, state = 1):
        self.client.send(Press_inter(self.name, state))
