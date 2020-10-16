from tree.utils.Liste import Liste
from random import randint
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
            # on ajoute aussi les variable de spotify
            vars()["bpm"] = Spotify.get_bpm()
            return eval(string)
        return 0


    def eval(self, string):
        try:
            return int(string)
        except:
            return self.int(string)

    def get(self, nom):
        return self.variables.get(nom)
