import numpy as np
from scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep

class Instruction_projecteur(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(this, projecteur, dimmeur, duree):
        Instruction_lumiere.__init__(this, projecteur, dimmeur, duree)

    def run(this):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = this.dimmeur
        dimmeur_initial = this.lumière.dimmeur
        nb_points = RESOLUTION*this.duree

        for dim in np.arange(dimmeur_initial, dimmeur_final, nb_points):
            this.lumière.set(dim)
            sleep(1/RESOLUTION)

    def show(this):
        print("projo = ",this.lumière.nom, " | dimmeur = ", this.dimmeur, " | duree = ", this.duree)
