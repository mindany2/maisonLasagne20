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
        # si on veut que le precent soit mis a false
        # et celui ci a on
        return None

    def __eq__(self, other):
        if isinstance(other, Bouton):
            return self.nom == other.nom
        return False

    def get_name(self):
        return self.nom

    def show(self):
        print("bouton "+self.nom)
