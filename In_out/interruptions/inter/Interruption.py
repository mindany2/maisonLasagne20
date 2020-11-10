from tree.utils.Liste import Liste
from utils.communication.interrupt.Press_inter import Press_inter
from utils.Logger import Logger
from tree.Tree import Tree
from time import time
from enum import Enum

class TYPE_INTER(Enum):
    extender = 0
    rpi = 1
    cron = 2

class Interruption:
    """
    Ceci est une interruption quelconque
    """
    # mode pousoir par défaut

    def __init__(self, nom, client, type_inter):
        self.nom = nom
        self.client = client
        self.type = type_inter


    def press(self, etat = 1):
        Logger.info("on press le bouton "+self.nom)
        self.client.send(Press_inter(self.nom, etat))

    def show(self):
        print(self.nom)

