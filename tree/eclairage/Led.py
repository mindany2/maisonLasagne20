from tree.eclairage.Lumiere import Lumiere
from tree.utils.Couleur import Couleur
from time import sleep
from random import randrange
from In_out.cartes.relais.Relais import Etat
from utils.Logger import Logger

class Led(Lumiere):
    """
    led en bluetooth
    """
    def __init__(self, nom, relais, controleur, couleur = 0):
        Lumiere.__init__(self, nom)
        self.couleur = Couleur(couleur)
        self.dimmeur = 0
        self.relais =  relais
        self.controleur = controleur
        self.connecté = False
        self.planté = False  # indique si la led à eu un problème dernièrement (pas de connection à l'éteignage)

    def connect(self):
        if not(self.connecté):
            Logger.info("on essaie de se co a "+self.nom)
            if self.couleur.is_black() or self.planté:
                self.relais.set(Etat.ON)
                sleep(1)
            self.planté = False
            self.connecté = not(self.controleur.connect())
        return not(self.connecté)

    def deconnect(self, planté = False):
        print(self.connecté)
        if self.connecté:
            sleep(0.5)
            self.controleur.deconnect(is_black = self.couleur.is_black())
            if self.couleur.is_black() or planté:
                self.planté = True
                self.relais.set(Etat.OFF)
            self.connecté = False
        # TODO on enregistre la couleur de la led

    def set(self, dimmeur, couleur):
        err1, err2 = 0,0
        if self.couleur != Couleur(couleur):
            self.couleur = Couleur(couleur)
            err1 = self.controleur.send_color(self.couleur)
        if self.dimmeur != dimmeur:
            self.dimmeur = dimmeur
            err2 = self.controleur.send_dimmeur(self.dimmeur)
        return (err1 or err2)
        #print(self.nom," met le dimmeur a ",self.dimmeur," de couleur ",str(self.couleur.valeur))

    def show(self):
        print("nom = " + self.nom," | couleur = ", self.couleur)
        self.relais.show()

