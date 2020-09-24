from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep, time
from utils.Logger import Logger

class Instruction_projecteur(Instruction_lumiere):
    """
    On set un projecteur
    """
    def __init__(self, projecteur, dimmeur, duree, temps_init, synchro):
        Instruction_lumiere.__init__(self, projecteur, dimmeur, duree, temps_init, synchro)

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        try:
            self.lumière.lock(self.id_liste)
            temps_init = time()
            dimmeur_initial = self.lumière.dimmeur
            dimmeur_final = self.eval(self.dimmeur)
            ecart = dimmeur_final - dimmeur_initial
            nb_points = self.eval(self.duree)*RESOLUTION

            if dimmeur_initial == dimmeur_final:
                Logger.info("on fait rien pour {}".format(self.lumière.nom))
                return

            self.lumière.connect()
            super().run(temps_ecouler=(time()-temps_init))
            barrier.wait()
            val = dimmeur_initial
            debut = time()
            for _ in range(0,nb_points):
                if self.lumière.test():
                    raise SystemExit("kill inst")
                temps = time()
                self.lumière.set(val)
                val += ecart/nb_points
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)
            self.lumière.set(dimmeur_final)
            Logger.info(" le projecteur {} a mis {} s a s'allumer au lieu de {}".format(self.lumière.nom, time()-debut, self.duree))

        finally:
            self.lumière.deconnect()
            self.lumière.unlock()

    def show(self):
        print("projo = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree)
