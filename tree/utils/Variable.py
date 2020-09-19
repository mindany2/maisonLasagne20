
class Variable:
    """
    Stocke juste une variable d'un environnement
    """
    def __init__(self, nom, val):
        self.nom = nom
        self.val = val

    def get(self):
        return self.val

    def set(self, val):
        self.val = val
        
