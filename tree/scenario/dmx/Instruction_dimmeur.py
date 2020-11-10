from tree.scenario.Instruction_lumiere import Instruction_lumiere
from time import sleep, time
import numpy as np
from utils.Logger import Logger
RESOLUTION = 10

class Instruction_dimmeur(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(self, lumière, dimmeur, duree, temps_init, synchro):
        Instruction_lumiere.__init__(self, lumière, dimmeur, duree, temps_init, synchro)

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run(temps_ecouler=0)
        try:
            self.lumière.lock_dimmeur()
            temps_init = time()
 
            dimmeur_initial = self.lumière.dimmeur
            dimmeur_final = self.eval(self.dimmeur)
            if self.duree == 0:
                return
            nb_points = RESOLUTION*self.duree
            if dimmeur_final != dimmeur_initial:
                liste = np.arange(dimmeur_initial, dimmeur_final, (dimmeur_final-dimmeur_initial)/nb_points)
            else:
                barrier.wait()
                Logger.info("On ne fait rien pour "+ self.lumière.nom)
                return

            barrier.wait()
            for dimmeur in liste:
                if self.lumière.test_dimmeur():
                    raise SystemExit("kill inst")
                temps = time()
                self.lumière.set_dimmeur(int(dimmeur))
                barrier.wait()
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)

        except SystemExit:
            Logger.info("L'instruction sur {} a ete kill".format(self.lumière.nom))

        finally:
            self.lumière.set_dimmeur(dimmeur_final)
            Logger.info("{} a mis 0s a s'allumer au lieu de {}".format(self.lumière.nom, self.duree))
            self.lumière.unlock_dimmer()

    def show(self):
        print("projo = ",self.lumière.nom, " | position = ", self.dimmeur, " | duree = ", self.duree)
