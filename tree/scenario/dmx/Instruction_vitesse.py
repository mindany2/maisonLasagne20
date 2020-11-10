from tree.scenario.Instruction import Instruction
from time import sleep, time
import numpy as np
from utils.Logger import Logger

class Instruction_vitesse(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, lumière, valeur, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.lumière = lumière
        self.valeur = valeur

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run(temps_ecouler=0)
        barrier.wait()
        self.lumière.set_vitesse(self.eval(self.valeur))

    def show(self):
        print("projo = ",self.lumière.nom, " | program = ", self.valeur, " | duree = ", self.duree)
