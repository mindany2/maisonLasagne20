from tree.eclairage.Lumiere import Lumiere
from tree.utils.Couleur import Couleur
from time import sleep
from random import randrange
from threading import Lock

from In_out.cartes.Relais import Relais, Etat

class Led(Lumiere):
    """
    led en bluetooth
    """
    def __init__(self, nom, relais, controleur, couleur = "0x000000"):
        Lumiere.__init__(self, nom)
        self.couleur = Couleur(couleur)
        self.dimmeur = 0
        self.relais =  relais
        self.controleur = controleur
        self.mutex = Lock()

    def connect(self):
        self.mutex.acquire()
        print("on essaie de se co a "+self.nom)
        if self.couleur.is_black() or self.dimmeur == 0:
            self.relais.set(Etat.ON)
            sleep(0.5)
            return self.controleur.connect()
        return 0
            


    def deconnect(self):
        if self.couleur.is_black():
            self.controleur.deconnect()
            sleep(0.5)
            self.relais.set(Etat.OFF)
        self.mutex.release()
        # TODO on enregistre la couleur de la led


    def set(self, dimmeur, couleur):
        if self.couleur != Couleur(couleur):
            self.couleur = Couleur(couleur)
            self.controleur.send_color(self.couleur.valeur)
        if self.dimmeur != dimmeur:
            self.dimmeur = dimmeur
            self.controleur.send_dimmeur(self.dimmeur)
        print(self.nom," met le dimmeur a ",self.dimmeur," de couleur ",str(self.couleur.valeur))

    def show(self):
        print("nom = " + self.nom," | couleur = ", self.couleur)
        self.relais.show()

