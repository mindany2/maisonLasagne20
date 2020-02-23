import numpy as np
from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep

class Instruction_projecteur(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(self, projecteur, dimmeur, duree, attente):
        Instruction_lumiere.__init__(self, projecteur, dimmeur, duree, attente)

    def run(self):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = self.dimmeur
        dimmeur_initial = self.lumière.dimmeur
        nb_points = RESOLUTION*self.duree

        for dim in np.arange(dimmeur_initial, dimmeur_final, nb_points):
            self.lumière.set(dim)
            sleep(1/RESOLUTION)

    def show(self):
        print("projo = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree)
