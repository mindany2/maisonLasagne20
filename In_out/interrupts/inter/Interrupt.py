from In_out.network.messages.interrupt.Press_inter import Press_inter
from tree.utils.Logger import Logger
from tree.Tree import Tree
from time import time

class Interrupt:
    """
    This is an interrupt for the interrupt process
    that send it's value to the tree process
    """

    def __init__(self, name, name_env, client):
        self.name = name
        self.name_env = name_env
        self.client = client

    def press(self, state = None):
        Logger.info("Press inter {} on {} with {}".format(self.name, self.name_env, state)) 
        self.client.send(Press_inter(self.name_env, self.name, state))

    def start(self):
        pass

    def __str__(self):
        return self.name
