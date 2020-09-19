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


    def run(self, barrier, save_valeurs=True, volume_ref = True):

        try:
            self.enceinte.lock()
            super().run()

            if volume_ref:
                self.enceinte.volume_ref = self.volume

            volume_initial = self.enceinte.volume
            volume_final = self.eval(self.volume)
            ecart = volume_final - volume_initial

            if ecart == 0:
                Logger.info("on fait rien pour l'enceinte {}".format(self.enceinte.nom))
                return
            nb_points = self.duree*RESOLUTION

            val = volume_initial
            debut = time()
            for _ in range(0,nb_points):
                temps = time()
                self.enceinte.change_volume(int(val), save_valeurs)
                val += ecart/nb_points
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)
            Logger.info(" l'enceinte {} a mis {} s a s'allumer au lieu de {}".format(self.enceinte.nom, time()-debut, self.duree))
            self.enceinte.change_volume(volume_final, save_valeurs)
        finally:
            self.enceinte.unlock()
            sleep(60) # on attend
            self.enceinte.ampli.eteindre() # on eteint si toutes les zones sont eteintes
 


