import numpy as np
from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep

class Instruction_projecteur(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(self, projecteur, dimmeur, duree, attente):
        Instruction_lumiere.__init__(self, projecteur, dimmeur, duree, attente)

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = self.dimmeur
        dimmeur_initial = self.lumière.dimmeur
        nb_points = RESOLUTION*self.duree
        print("dimmeur_initial  = ", dimmeur_initial, " / dimmeur_final = ", dimmeur_final)
        print( nb_points)
        if dimmeur_initial != dimmeur_final:
            liste = np.arange(dimmeur_initial, dimmeur_final, (dimmeur_final-dimmeur_initial)/nb_points)
        else:
            liste = [0]*nb_points
        barrier.wait()
        for dimmeur in liste:
            self.lumière.set(int(dimmeur))
            sleep(1/RESOLUTION)

        self.lumière.set(dimmeur_final)

    def show(self):
        print("projo = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree)
