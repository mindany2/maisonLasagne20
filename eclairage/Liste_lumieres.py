from eclairage.Lumiere import Lumiere

class Liste_lumieres:
    """
    Contient le dictionnaire qui lie les
    lumières et leur nom
    """
    def __init__(self):
        self.dictionnaire = dict()

    def add(self, lumière):
        self.dictionnaire[lumière.nom] = lumière

    def get(self, nom):
        return self.dictionnaire[nom]

    def show(self):
        for lum in self.dictionnaire.values():
            lum.show()
