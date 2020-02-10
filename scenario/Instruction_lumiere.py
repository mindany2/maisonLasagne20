from scenario.Instruction import Instruction, Attente
from eclairage.Lumiere import Lumiere

RESOLUTION = 10

class Instruction_lumiere(Instruction):
    """
    Une instruction de type allumage
    """
    def __init__(this, lumière, dimmeur, duree):
        Instruction.__init__(this)
        this.dimmeur = dimmeur
        this.vitesse = duree
        this.lumière = lumière

