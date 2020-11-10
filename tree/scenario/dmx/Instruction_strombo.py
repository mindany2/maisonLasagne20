from tree.scenario.Instruction import Instruction
from time import sleep, time
import numpy as np
from utils.Logger import Logger

class Instruction_strombo(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, lumière, strombo, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.lumière = lumière
        self.strombo = strombo

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run(temps_ecouler=0)
        barrier.wait()
        self.lumière.set_strombo(self.strombo)

    def show(self):
        print("projo = ",self.lumière.nom, " | strombo = ", self.strombo, " | duree = ", self.duree)
