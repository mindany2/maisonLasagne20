import numpy as np
from scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep

class Instruction_projecteur(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(self, projecteur, dimmeur, duree):
        Instruction_lumiere.__init__(self, projecteur, dimmeur, duree)

    def run(self):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = self.dimmeur
        dimmeur_initial = self.projecteur.dimmeur
        nb_points = RESOLUTION*duree

        for dim in np.arange(dimmeur_initial, dimmeur_final, nb_points):
            projecteur.set(dim)
            sleep(1/RESOLUTION)

    def show(self):
        print("projo = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree)
