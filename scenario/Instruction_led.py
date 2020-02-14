import numpy as np
from scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from eclairage.Led import Couleur
from time import sleep

class Instruction_led(Instruction_lumiere):
    """
    On set une bande de led
    """
    def __init__(self, led, dimmeur, duree, couleur):
        Instruction_lumiere.__init__(self, led, dimmeur, duree)
        self.couleur = couleur

    def run(self):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = self.dimmeur
        dimmeur_initial = self.lumière.dimmeur
        nb_points = RESOLUTION*self.duree
        liste_dimmeur = np.arange(dimmeur_initial, dimmeur_final, nb_points)
        print("couleur = ",str(self.lumière.couleur)," couleur voulut = ",self.couleur),
        couleur_final = Couleur(self.couleur)
        liste_couleur = np.arange(self.lumière.couleur.valeur, couleur_final.valeur, nb_points)
        print(liste_couleur)

        for dim, valeur_couleur in zip(liste_dimmeur, liste_couleur):
            self.lumière.set(dim, valeur_couleur)
            sleep(1/RESOLUTION)
    
    def show(self):
        print("led = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree, " | couleur = ",self.couleur)

