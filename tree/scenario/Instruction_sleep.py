from tree.scenario.Instruction import Instruction,Attente
from time import sleep

class Instruction_sleep(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, duree):
        Instruction.__init__(self, Attente.WAIT, duree)
        self.duree = duree

    def run(self):
        """
        On s'occupe de faire l'instruction
        """
        sleep(self.duree)

    def show(self):
        print("sleep "," | duree = ", self.duree)
