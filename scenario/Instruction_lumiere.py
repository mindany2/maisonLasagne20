from scenario.Instruction import Instruction, Attente
from eclairage.Lumiere import Lumiere

RESOLUTION = 10

class Instruction_lumiere(Instruction):
    """
    Une instruction de type allumage
    """
    def __init__(this, lumière, dimmeur, duree, attente = Attente.CONTINUE):
        Instruction.__init__(this, duree, attente)
        this.dimmeur = dimmeur
        this.duree = duree
        this.lumière = lumière

