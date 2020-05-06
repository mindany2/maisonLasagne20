from tree.utils.Liste import Liste
from tree.Tree import Tree
from time import time
from threading import Lock

class Interrupteur:
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin):
        self.nom = nom
        self.pin = pin
        self.temps = time() 
        self.mutex = Lock()


    def press(self):
        if ((time() - self.temps) > 1):     # permet de prendre que le premier appuie
            print("on press le bouton "+self.nom)
            Tree().press_inter(self.nom)
            self.temps = time() 

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

