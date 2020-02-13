import numpy as np
from scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep

class Instruction_led(Instruction_lumiere):
    """
    On set une bande de led
    """
    def __init__(this, led, dimmeur, duree, couleur):
        Instruction_lumiere.__init__(this, led, dimmeur, duree)
        this.couleur = couleur

    def run(this):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = this.dimmeur
        dimmeur_initial = this.projecteur.dimmeur
        nb_points = RESOLUTION*duree
        liste_dimmeur = np.arange(dimmeur_initial, dimmeur_final, nb_points)
        liste_couleur = np.arange(this.led.couleur, this.couleur, nb_points)

        for dim, couleur in zip(liste_dimmeur, liste_couleur):
            led.set(dim, couleur)
            sleep(1/RESOLUTION)
    
    def show(this):
        print("led = ",this.lumière.nom, " | dimmeur = ", this.dimmeur, " | duree = ", this.duree, " | couleur = ",this.couleur)

