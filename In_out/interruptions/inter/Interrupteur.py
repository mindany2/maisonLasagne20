from time import time
from tree.Tree import Tree
from In_out.interruptions.inter.Interruption import Interruption
from utils.Logger import Logger
from utils.communication.Press_inter import Press_inter

class Interrupteur(Interruption):
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin, client, type_inter):
        Interruption.__init__(self, nom, pin, client, type_inter)
        self.temps = time()

    def press(self, etat = 1):
        if ((time() - self.temps) > 1):     # permet de prendre que le premier appuie
            Logger.info("on press le bouton "+self.nom)
            self.client.send(Press_inter(self.nom, etat))
            
            self.temps = time() 

    def show(self):
        print(self.nom + " : " + str(self.pin) + " : ")

