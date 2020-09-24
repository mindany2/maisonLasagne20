from tree.scenario.Instruction import Instruction
from utils.Logger import Logger
from time import time, sleep

RESOLUTION = 10

class Instruction_enceinte(Instruction):
    """
    Une instruction appellant un bouton d'un autre environnement
    """
    def __init__(self, enceinte, volume, duree, temps_init, synchro):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.volume = volume
        self.enceinte = enceinte


    def run(self, barrier):

        debut = time()
        try:
            self.enceinte.lock()
            super().run()

            volume_initial = self.enceinte.volume()
            volume_final = self.eval(self.volume)
            ecart = volume_final - volume_initial

            if ecart == 0:
                Logger.info("on fait rien pour l'enceinte {}".format(self.enceinte.nom))
                return
            nb_points = self.duree*RESOLUTION
            self.enceinte.connect()

            val = volume_initial
            for _ in range(0,nb_points):
                if self.enceinte.test():
                    raise SystemExit("kill inst")
                temps = time()
                self.enceinte.change_volume(int(val))
                val += ecart/nb_points
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)
            self.enceinte.change_volume(volume_final)
            self.enceinte.deconnect()
        finally:
            Logger.info(" l'enceinte {} a mis {} s a s'allumer au lieu de {}".format(self.enceinte.nom, time()-debut, self.duree))
            self.enceinte.unlock()
 


