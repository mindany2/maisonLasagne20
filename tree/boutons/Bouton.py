class Bouton:
    """
    La base d'un bouton
    """

    def __init__(self, nom):
        self.nom = nom

    def etat(self):
        return False

    def press(self):
        """
        Lance le bon scénario et gère la pile
        """

    def __eq__(self, other):
        if isinstance(other, Bouton):
            return self.nom == other.nom
        return False

    def get_name(self):
        return self.nom

    def show(self):
        print("bouton "+self.nom)
