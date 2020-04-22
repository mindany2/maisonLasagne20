import numpy as np
from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from tree.eclairage.Led import Couleur
from time import sleep

class Instruction_led(Instruction_lumiere):
    """
    On set une bande de led
    """
    def __init__(self, led, dimmeur, duree, temps_init, synchro, couleur):
        Instruction_lumiere.__init__(self, led, dimmeur, duree, temps_init, synchro)
        self.couleur = Couleur(couleur)

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        dimmeur_final = self.dimmeur
        dimmeur_initial = self.lumière.dimmeur
        nb_points = RESOLUTION*self.duree
        print("couleur = ",str(self.lumière.couleur)," couleur voulut = ",self.couleur),
        if dimmeur_initial != dimmeur_final:
            liste_dimmeur = np.arange(dimmeur_initial, dimmeur_final, (dimmeur_final-dimmeur_initial)/nb_points)
        else:
            liste_dimmeur = [0]*nb_points

        if self.couleur != self.lumière.couleur:
            liste_couleur = self.couleur.generate_array(self.lumière.couleur, nb_points)
        else:
            print("on fait rien")
            barrier.wait()
            return

        err = self.lumière.connect()
        if err:
            print("l'instruction sur "+self.lumière.nom+" a planté")
            barrier.wait()
            self.lumière.deconnect()
            return



        barrier.wait()
        for dim, valeur_couleur in zip(liste_dimmeur, liste_couleur):
            if not(err):
                self.lumière.set(int(dim), valeur_couleur)
            sleep(1/RESOLUTION)
            barrier.wait()

        if not(err):
            self.lumière.set(int(dimmeur_final), self.couleur.valeur)
            sleep(3)
        self.lumière.deconnect()
    
    def show(self):
        print("led = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree, " | couleur = ",self.couleur)

