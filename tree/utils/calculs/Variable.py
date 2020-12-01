
class Variable:
    """
    Store a value
    """
    def __init__(self, nom, val):
        self.nom = nom
        self.val = val

    def get(self, args = None):
        return self.val

    def set(self, val):
        self.val = val
        
    def __int__(self):
        return self.get()

    def __add__(self, integer):
        return int(self)+integer
