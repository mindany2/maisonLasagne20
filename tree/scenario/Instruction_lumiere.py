from tree.scenario.Instruction import Instruction, Attente
from tree.eclairage.Lumiere import Lumiere

RESOLUTION = 30

class Instruction_lumiere(Instruction):
    """
    Une instruction de type allumage
    """
    def __init__(self, lumière, dimmeur, duree, attente):
        Instruction.__init__(self, duree, attente)
        self.dimmeur = dimmeur
        self.duree = duree
        self.lumière = lumière

