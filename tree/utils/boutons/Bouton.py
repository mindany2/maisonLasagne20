class Bouton:
    """
    La base d'un bouton
    """

    def __init__(self, nom):
        self.nom = nom

    def etat(self):
        return False

    def press(self):
        pass

    def show(self):
        print("bouton "+self.nom)
