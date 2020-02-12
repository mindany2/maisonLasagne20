from scenario.Instruction import Instruction,Attente
from time import sleep

class Instruction_projecteur(Instruction):
    """
    On set un projecteur
    """
    def __init__(this):
        Instruction.__init__(this, Attente.WAIT, duree)
        this.duree = duree

    def run(this):
        """
        On s'occupe de faire l'instruction
        """
        sleep(this.duree)

