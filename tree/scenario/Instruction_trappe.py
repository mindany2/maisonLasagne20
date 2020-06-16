from tree.eclairage.Trappe import Trappe
from tree.scenario.Instruction import Instruction

LISTE_ACTIONS = ["monte", "descent", "verrouille", "deverrouille"]

class Instruction_trappe(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, action, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.action = action
        assert(LISTE_ACTIONS.count(action)) # on verifie que c'est dans la liste

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run()
        if self.action == "monte":
            Trappe().ouvre()
        elif self.action == "descent":
            Trappe().ferme()
        elif self.action == "verrouille":
            Trappe().set_secu(True)
        elif self.action == "deverrouille":
            Trappe().set_secu(False)
        print("on {} la trappe".format(self.action))


    def show(self):
        print("on {} la trappe a {}".format(self.action, self.temps_init))
