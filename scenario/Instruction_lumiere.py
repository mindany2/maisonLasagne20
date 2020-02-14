from scenario.Instruction import Instruction, Attente
from eclairage.Lumiere import Lumiere

RESOLUTION = 10

class Instruction_lumiere(Instruction):
    """
    Une instruction de type allumage
    """
    def __init__(self, lumière, dimmeur, duree, attente = Attente.CONTINUE):
        Instruction.__init__(self, duree, attente)
        self.dimmeur = dimmeur
        self.duree = duree
        self.lumière = lumière

