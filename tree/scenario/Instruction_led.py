import numpy as np
from tree.scenario.Instruction_lumiere import Instruction_lumiere, RESOLUTION
from tree.eclairage.Led import Couleur
from time import sleep

class Instruction_led(Instruction_lumiere):
    """
    On set une bande de led
    """
    def __init__(self, led, dimmeur, duree, couleur, attente):
        Instruction_lumiere.__init__(self, led, dimmeur, duree, attente)
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

        try:
            liste_couleur = self.couleur.generate_array(self.lumière.couleur, nb_points)
        except ZeroDivisionError:
            print("on fait rien")
            barrier.wait()
            return

        err = self.lumière.connect()
        if err:
            print("l'instruction sur "+self.lumière.nom)


        print("on attend")
        barrier.wait()
        print("on part !!!")
        for dim, valeur_couleur in zip(liste_dimmeur, liste_couleur):
            self.lumière.set(dim, valeur_couleur)
            sleep(1/RESOLUTION)
            barrier.wait()

        self.lumière.set(dimmeur_final, self.couleur.valeur)
        sleep(1.5)
        self.lumière.deconnect()
    
    def show(self):
        print("led = ",self.lumière.nom, " | dimmeur = ", self.dimmeur, " | duree = ", self.duree, " | couleur = ",self.couleur)

