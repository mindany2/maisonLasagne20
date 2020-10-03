from tree.utils.Liste import Liste
from random import randint
from tree.Tree import Tree
from tree.scenario.Scenario import MARQUEUR
from utils.spotify.Spotify import Spotify

class Calculateur:
    """
    Permet de calculer des expression régulière
    """
    def __init__(self):
        self.variables = Liste()

    def add(self, var):
        self.variables.add(var)

    def int(self, string):
        if string != "":
            for var in self.variables:
                vars()[var.nom] = var.get()
            for env in Tree().liste_envi:
                vars()[env.nom+"_etat"] = (env.etat() == MARQUEUR.ON)
                for var in env.calculateur.variables:
                    vars()[env.nom+"_"+var.nom] = var.get()
            vars()["volume_spotify"] = Spotify().volume
            vars()["etat_spotify"] = Spotify().etat
            return eval(string)
        return 0


    def eval(self, string):
        try:
            return int(string)
        except:
            return self.int(string)

    def get(self, nom):
        return self.variables.get(nom)
