import numpy as np
from scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from eclairage.Led import Couleur
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
        dimmeur_initial = this.lumière.dimmeur
        nb_points = RESOLUTION*this.duree
        liste_dimmeur = np.arange(dimmeur_initial, dimmeur_final, nb_points)
        print("couleur = ",str(this.lumière.couleur)," couleur voulut = ",this.couleur),
        couleur_final = Couleur(this.couleur)
        liste_couleur = np.arange(this.lumière.couleur.valeur, couleur_final.valeur, nb_points)
        print(liste_couleur)

        for dim, valeur_couleur in zip(liste_dimmeur, liste_couleur):
            this.lumière.set(dim, valeur_couleur)
            sleep(1/RESOLUTION)
    
    def show(this):
        print("led = ",this.lumière.nom, " | dimmeur = ", this.dimmeur, " | duree = ", this.duree, " | couleur = ",this.couleur)

