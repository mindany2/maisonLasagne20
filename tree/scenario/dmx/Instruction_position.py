from tree.scenario.Instruction import Instruction
from time import sleep, time
import numpy as np
from utils.Logger import Logger
RESOLUTION = 10

class Instruction_position(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, lumière, position_final, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.position_final = position_final
        self.lumière = lumière

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        try:
            super().run(temps_ecouler=0)
            self.lumière.lock(self.id_liste)
            temps_init = time()
 
            x_init, y_init = self.lumière.get_position()
            x_final, y_final = self.eval(self.position_final)
            if self.duree == 0:
                return
            nb_points = RESOLUTION*self.duree
            if x_init != x_final:
                liste_x = np.arange(x_init, x_final, (x_final-x_init)/nb_points)
            else:
                liste_x = [x_init]*int(nb_points)
            if y_init != y_final:
                liste_y = np.arange(y_init, y_final, (y_final-y_init)/nb_points)
            else:
                liste_y = [y_init]*int(nb_points)

            barrier.wait()
            for x, y in zip(liste_x, liste_y):
                temps = time()
                if self.lumière.test():
                    raise SystemExit("kill inst")
                self.lumière.set_position(int(x), int(y))
                barrier.wait()
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)

        except SystemExit:
            Logger.info("L'instruction sur {} a ete kill".format(self.lumière.nom))

        finally:
            Logger.info("{} a mis {} s a se deplacer au lieu de {}".format(self.lumière.nom, time()-temps_init, self.duree))
            self.lumière.set_position(x_final, y_final)
            self.lumière.unlock()

    def show(self):
        print("projo = ",self.lumière.nom, " | position = ", self.position_final, " | duree = ", self.duree)
