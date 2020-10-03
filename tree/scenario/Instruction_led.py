import numpy as np
from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from tree.eclairage.Led import Couleur
from time import sleep,time
from utils.Logger import Logger

class Instruction_led(Instruction_lumiere):
    """
    On set une bande de led
    """
    def __init__(self, led, dimmeur, duree, temps_init, synchro, couleur):
        Instruction_lumiere.__init__(self, led, dimmeur, duree, temps_init, synchro)
        self.couleur = couleur

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        temps_init = time()
        err, err1 = False, False

        try:
            self.lumière.lock(self.id_liste)
     
            dimmeur_final = self.eval(self.dimmeur)
            dimmeur_initial = self.lumière.dimmeur
            nb_points = RESOLUTION*self.eval(self.duree)
            couleur = Couleur(self.eval(self.couleur))
            if dimmeur_initial != dimmeur_final:
                liste_dimmeur = np.arange(dimmeur_initial, dimmeur_final, (dimmeur_final-dimmeur_initial)/nb_points)
            else:
                liste_dimmeur = [dimmeur_initial]*nb_points
            if couleur != self.lumière.couleur:
                liste_couleur = couleur.generate_array(self.lumière.couleur, nb_points)
            else:
                #Logger.debug("on fait rien pour {}".format(self.lumière.nom))
                self.lumière.deconnect() # on la deco si besoin
                barrier.wait()
                return

            err = self.lumière.connect()
            if err:
                Logger.debug("l'instruction sur "+self.lumière.nom+" a planté")
                barrier.wait()
                self.lumière.deconnect(planté = True)
                return
            super().run(temps_ecouler=(time()-temps_init))



            barrier.wait()
            for dim, valeur_couleur in zip(liste_dimmeur, liste_couleur):
                if self.lumière.test():
                    raise SystemExit("kill inst")
                if not(err):
                    err1 = self.lumière.set(dim, valeur_couleur)
                    if err1:
                        break
                sleep(1/RESOLUTION)
                barrier.wait()
            if (not(err) and not(err1)):
                self.lumière.set(dimmeur_final, couleur.valeur)
                self.lumière.deconnect()

        finally:
            Logger.info(" la led {} a mis {} s a s'allumer au lieu de {}".format(self.lumière.nom, time()-temps_init, self.duree))
            self.lumière.unlock()
    
    def show(self):
        print("led = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree, " | couleur = ",self.couleur)


