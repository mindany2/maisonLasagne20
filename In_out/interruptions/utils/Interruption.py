from tree.utils.Liste import Liste
from tree.Tree import Tree
from time import time

class Interruption:
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin, client):
        self.nom = nom
        self.pin = pin
        self.client = client


    def press(self):
        pass

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

