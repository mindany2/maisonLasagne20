from tree.utils.Liste import Liste
from tree.Tree import Tree
from time import time
from enum import Enum

class TYPE_INTER(Enum):
    extender = 0

class Interruption:
    """
    Ceci est une interruption quelconque
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin, client, type_inter):
        self.nom = nom
        self.pin = pin
        self.client = client
        self.type = type_inter


    def press(self):
        pass

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

