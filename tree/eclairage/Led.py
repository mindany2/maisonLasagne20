from tree.eclairage.Lumiere import Lumiere
from tree.eclairage.Couleur import Couleur
from time import sleep
from random import randrange

from utils.In_out.Bluetooth import Bluetooth
from utils.In_out.controle.Relais import Relais, Etat

class Led(Lumiere):
    """
    led en bluetooth
    """
    def __init__(self, nom, relais, bluetooth_addr, type_controler, couleur = "0x000000"):
        Lumiere.__init__(self, nom)
        self.couleur = Couleur(couleur)
        self.relais =  relais
        self.bluetooth = Bluetooth(bluetooth_addr, type_controler)

    def connect(self):
        if self.couleur.is_black():
            self.relais.set(Etat.ON)
        err = 1
        compteur = 0
        while err and compteur < 10:
            err = self.bluetooth.connect()
            if err:
                compteur += 1
                print(self.nom +" n'arrive pas a se connecter ")
                sleep(1)
        if compteur == 10:
            return 1
        return 0
            


    def deconnect(self):
        try:
            self.bluetooth.deconnect()
        except:
            pass
        if self.couleur.is_black():
            self.relais.set(Etat.OFF)
        # TODO on enregistre la couleur de la led


    def set(self, dimmeur, couleur):
        if self.couleur != Couleur(couleur):
            self.bluetooth.send_color(self.couleur.valeur)
        self.dimmeur = dimmeur
        self.couleur = Couleur(couleur)
        print(self.nom," met le dimmeur a ",dimmeur," de couleur ",str(couleur))

    def show(self):
        print("nom = " + self.nom," | couleur = ", self.couleur)
        self.relais.show()

