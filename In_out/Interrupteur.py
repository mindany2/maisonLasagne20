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
        self.bouton = None
        self.used = False    # permet de prendre que 1 appuie
        self.mutex = Lock()


    def set_bouton(self, bouton):
        self.bouton = bouton

    def press(self):
        if not(self.used):
            self.used = True
            print("on press le bouton "+self.nom)
            self.bouton.press()
            sleep(2)
            self.used = False

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")
        self.bouton.show()

