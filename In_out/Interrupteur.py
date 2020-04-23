from tree.utils.Liste import Liste
from tree.Tree import Tree
from time import sleep
from threading import Lock

class Interrupteur:
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin):
        self.nom = nom
        self.pin = pin
        self.used = False    # permet de prendre que 1 appuie
        self.mutex = Lock()


    def press(self):
        if not(self.used):
            self.used = True
            print("on press le bouton "+self.nom)
            Tree().press_inter(self.nom)
            sleep(2)
            self.used = False

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

