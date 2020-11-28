from tree.eclairage.Trappe import ETAT
from tree.scenario.Instruction import Instruction
from enum import Enum
from time import time, sleep

class INST_TRAPPE(Enum):
    monter = 1
    descendre = 2

class Instruction_trappe(Instruction):
    """
    On set un projecteur
    """
    def __init__(self,trappe, action, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.action = action
        self.trappe = trappe

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        try:
            print("on lock")
            self.trappe.lock(self.id_liste)
            print("on est lock")
            if self.action == INST_TRAPPE.descendre and self.trappe.etat != ETAT.bas:
                # on descend
                self.trappe.set_aimant(False)
                if self.trappe.etat == ETAT.haut:
                    self.trappe.change(ETAT.en_cours)
                    super().run()

                if self.trappe.test():
                    # on m'a kill
                    raise SystemExit("kill inst")
                self.trappe.descendre()
                temps = time()
                while(time()-temps < self.eval(self.duree)):
                    sleep(0.1)
                    if self.trappe.test():
                        raise SystemExit("kill inst")
                self.trappe.change(ETAT.bas)

            elif self.action == INST_TRAPPE.monter and self.trappe.etat != ETAT.haut:
                # on monte
                if self.trappe.etat == ETAT.bas:
                    self.trappe.change(ETAT.en_cours)
                    super().run()

                if self.trappe.test():
                    # on m'a kill
                    raise SystemExit("kill inst")
                self.trappe.monter()
                self.trappe.set_aimant(True)
                temps = time()
                while(time()-temps < self.eval(self.duree)):
                    sleep(0.1)
                    if self.trappe.test():
                        raise SystemExit("kill inst")
                self.trappe.change(ETAT.haut)

        finally:
            print("la trappe est {}".format(self.trappe.etat))
            self.trappe.unlock()








    def eclairage(self):
        return self.trappe

    def show(self):
        print("on {} la trappe a {}".format(self.action, self.temps_init))
