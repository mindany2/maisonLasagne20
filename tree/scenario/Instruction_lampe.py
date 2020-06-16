import numpy as np
from tree.scenario.Instruction_lumiere import Instruction_lumiere
from time import sleep

class Instruction_lampe(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(self, lampe, dimmeur, temps_init, synchro, duree = 0):
        Instruction_lumiere.__init__(self, lampe, dimmeur, duree, temps_init, synchro)

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run()
        if self.lumière.etat() != (self.dimmeur != 0):
            self.lumière.set(self.dimmeur != 0)
        print("on met la lampe {} a {}".format(self.lumière, self.dimmeur))


    def show(self):
        print("projo = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree)
