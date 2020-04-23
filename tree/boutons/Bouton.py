class Bouton:
    """
    La base d'un bouton
    """

    def __init__(self, nom):
        self.nom = nom

    def etat(self):
        return False

    def press(self):
        # doit retourner le scénario qui à été lancer
        return None

    def get_name(self):
        return self.nom

    def show(self):
        print("bouton "+self.nom)
