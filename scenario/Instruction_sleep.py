from scenario.Instruction import Instruction,Attente
from time import sleep

class Instruction_sleep(Instruction):
    """
    On set un projecteur
    """
    def __init__(this, duree):
        Instruction.__init__(this, Attente.WAIT, duree)
        this.duree = duree

    def run(this):
        """
        On s'occupe de faire l'instruction
        """
        sleep(this.duree)

    def show(this):
        print("sleep "," | duree = ", this.duree)
