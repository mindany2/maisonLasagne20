from tree.eclairage.Lumiere import Lumiere
from tree.utils.Couleur import Couleur
from time import sleep
from random import randrange
from In_out.cartes.relais.Relais import Etat
from In_out.wifi_devices.Wifi_device import Wifi_device
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
        self.force = False

    def force_relais(self, force):
        # oblige à mettre le relais ON
        self.force = force
        if force:
            self.relais.set(Etat.ON)
        elif not(self.connecté):
            self.relais.set(Etat.OFF)

    def repair(self):
        if isinstance(self.controleur, Wifi_device):
            Logger.info("On tente de se connecté a "+self.nom)
            self.relais.set(Etat.ON)
            hs = self.controleur.connect(tentative = 5)
            if hs:
                Logger.error("La led {} est HS".format(self.nom))
                for _ in range(0,3):
                    self.relais.set(Etat.OFF)
                    sleep(3)
                    self.relais.set(Etat.ON)
                    sleep(3)
                return True
            self.deconnect()
            self.relais.set(Etat.OFF)
        return False

        

    def connect(self):
        if not(self.connecté):
            Logger.info("on essaie de se co a "+self.nom)
            if self.couleur.is_black() and not(self.force):
                self.relais.set(Etat.ON)
                sleep(1)
            self.connecté = not(self.controleur.connect())
            if not(self.connecté):
                # la led à planté
                self.relais.set(Etat.OFF)
        return not(self.connecté)

    def deconnect(self, planté = False):
        if self.connecté:
            sleep(3)
            self.controleur.deconnect(is_black = self.couleur.is_black())
            if self.couleur.is_black() and not(self.force):
                self.relais.set(Etat.OFF)
            self.connecté = False
        # TODO on enregistre la couleur de la led

    def set(self, dimmeur, couleur):
        err1, err2 = 0,0
        if self.couleur != Couleur(couleur, dimmeur):
            self.couleur = Couleur(couleur, dimmeur)
            err1 = self.controleur.send_color(self.couleur)
        if self.dimmeur != dimmeur:
            self.dimmeur = dimmeur
            err2 = self.controleur.send_dimmeur(self.dimmeur)
        return (err1 or err2)
        #print(self.nom," met le dimmeur a ",self.dimmeur," de couleur ",str(self.couleur.valeur))

    def show(self):
        print("nom = " + self.nom," | couleur = ", self.couleur)
        self.relais.show()

