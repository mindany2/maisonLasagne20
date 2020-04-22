from tree.scenario.Instruction import Instruction, Attente
from tree.eclairage.Lumiere import Lumiere

RESOLUTION = 10

class Instruction_lumiere(Instruction):
    """
    Une instruction de type allumage
    """
    def __init__(self, lumière, dimmeur, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.dimmeur = dimmeur
        self.duree = duree
        self.lumière = lumière

