from tree.utils.Liste import Liste
from random import randint

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
            return eval(string)
        return 0


    def eval(self, string):
        try:
            return int(string)
        except:
            return self.int(string)

    def get(self, nom):
        return self.variables.get(nom)
