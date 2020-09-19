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
        self.lumière = lumière

    def run(self, temps_ecouler=0):
        super().run(temps_ecouler)
        self.dimmeur = self.eval(self.dimmeur)

    def eclairage(self):
        return self.lumière

    def __eq__(self, other):
        if isinstance(other, Instruction_lumiere):
            return (self.dimmeur == other.dimmeur) and (self.lumière == other.lumière) 

        return False
