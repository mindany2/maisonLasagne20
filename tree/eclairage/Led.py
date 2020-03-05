from tree.eclairage.Lumiere import Lumiere
from commande.Relais import Relais, Etat
from commande.Bluetooth import Bluetooth
from time import sleep
import numpy as np

def rgb_to_hexa(r, g, b):
    return hex(r).zfill(2)+hex(g)[2:4].zfill(2)+hex(b)[2:4].zfill(2)

class Couleur:
    """
    Permet d'avoir la couleur en rgb
    """
    def __init__(self, hexa):
        self.valeur = hexa

    def set(self, couleur):
        self.valeur = couleur.valeur

    def int_to_rgb(self):
        print(self.valeur)
        self.r = int("0x"+self.valeur[2:4].zfill(2),16)
        self.g = int("0x"+self.valeur[4:6].zfill(2),16)
        self.b = int("0x"+self.valeur[6:8].zfill(2),16)
        print(self.r, self.g, self.b)

    def get_liste(self, variable_init, variable_self, nb_points):
        if variable_init != variable_self:
            return np.arange(variable_init, variable_self, float((variable_self - variable_init))/nb_points)
        return [0]*nb_points



    def __str__(self):
        return str(self.valeur)

    def generate_array(self, couleur_init, nb_points):
        self.int_to_rgb()
        print(nb_points)
        couleur_init.int_to_rgb()
        liste_rouge = self.get_liste(couleur_init.r, self.r, nb_points)
        liste_vert = self.get_liste(couleur_init.g, self.g, nb_points)
        liste_bleu = self.get_liste(couleur_init.b, self.b, nb_points)
        return [rgb_to_hexa(int(r),int(g),int(b)) for r,g,b in zip(liste_rouge, liste_vert, liste_bleu)]

    def is_black(self):
        return self.valeur == "0x000000"
    


class Led(Lumiere):
    """
    led en bluetooth
    """
    def __init__(self, nom, relais, bluetooth_addr, type_controler, couleur = "0x000000"):
        Lumiere.__init__(self, nom)
        self.relais =  relais
        self.couleur = Couleur(couleur)
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
                sleep(0.2)
        if compteur == 10:
            return 1
        return 0
            


    def deconnect(self):
        self.bluetooth.deconnect()
        if self.couleur.is_black():
            self.relais.set(Etat.OFF)


    def set(self, dimmeur, couleur):
        self.dimmeur = dimmeur
        self.couleur = Couleur(couleur)
        self.bluetooth.send(self.couleur.valeur)
        print(self.nom," met le dimmeur a ",dimmeur," de couleur ",str(couleur))

    def show(self):
        print("nom = " + self.nom," | bluetooth_addr = ",self.bluetooth.addr, " | couleur = ", self.couleur)
        self.relais.show()

