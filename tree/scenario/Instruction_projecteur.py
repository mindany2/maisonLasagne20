from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from time import sleep, time

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
        self.lumière.lock()
        temps_init = time()
        dimmeur_initial = self.lumière.dimmeur
        dimmeur_final = self.dimmeur
        ecart = dimmeur_final - dimmeur_initial
        nb_points = self.duree*RESOLUTION
        #print("dimmeur_initial  = ", dimmeur_initial, " / dimmeur_final = ", dimmeur_final)

        if dimmeur_initial == dimmeur_final:
            print("on fait rien pour {}".format(self.lumière.nom))
            self.lumière.unlock()
            return

        self.lumière.connect()
        super().run(temps_ecouler=(time()-temps_init))
        barrier.wait()
        val = dimmeur_initial
        debut = time()
        for _ in range(0,nb_points):
            temps = time()
            self.lumière.set(val)
            val += ecart/nb_points
            dodo = 1/RESOLUTION-(time()-temps)
            if dodo > 0:
                sleep(dodo)
        print(" le projecteur {} a mis {} s a s'allumer au lieu de {}".format(self.lumière.nom, time()-debut, self.duree))
        self.lumière.set(dimmeur_final)
        self.lumière.deconnect()
        self.lumière.unlock()


    def show(self):
        print("projo = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree)
