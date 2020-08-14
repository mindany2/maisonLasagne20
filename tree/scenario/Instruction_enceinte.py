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

        self.enceinte.lock()
        super().run()
        volume_initial = self.enceinte.volume
        volume_final = self.volume
        ecart = volume_final - volume_initial
        nb_points = self.duree*RESOLUTION

        val = volume_initial
        debut = time()
        for _ in range(0,nb_points):
            temps = time()
            self.enceinte.change_volume(int(val))
            val += ecart/nb_points
            dodo = 1/RESOLUTION-(time()-temps)
            if dodo > 0:
                sleep(dodo)
        Logger.info(" l'enceinte {} a mis {} s a s'allumer au lieu de {}".format(self.enceinte.nom, time()-debut, self.duree))
        self.enceinte.change_volume(volume_final)
        self.enceinte.unlock()
 


