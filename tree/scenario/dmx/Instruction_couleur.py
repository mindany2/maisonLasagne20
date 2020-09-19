from tree.scenario.Instruction import Instruction
from tree.eclairage.dmx.Lyre import COULEUR
from time import sleep, time
import numpy as np
from utils.Logger import Logger

class Instruction_couleur(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, lumière, couleur, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.lumière = lumière
        self.couleur = couleur

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run(temps_ecouler=0)
        barrier.wait()
        liste = [i.name for i in COULEUR]
        self.lumière.set_couleur(COULEUR[liste[self.eval(self.couleur)]])

    def show(self):
        print("projo = ",self.lumière.nom, " | couleur = ", self.couleur, " | duree = ", self.duree)
