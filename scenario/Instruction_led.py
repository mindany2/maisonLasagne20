import numpy as np
from scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
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
        dimmeur_initial = self.projecteur.dimmeur
        nb_points = RESOLUTION*duree
        liste_dimmeur = np.arange(dimmeur_initial, dimmeur_final, nb_points)
        liste_couleur = np.arange(self.led.couleur, self.couleur, nb_points)

        for dim, couleur in zip(liste_dimmeur, liste_couleur):
            led.set(dim, couleur)
            sleep(1/RESOLUTION)
    
    def show(self):
        print("led = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree, " | couleur = ",self.couleur)

