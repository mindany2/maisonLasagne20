
class Mode:
    """
    Ceci est un mode qui permet de changer rapidement
    de preset
    """
    def __init__(self, nom):
        self.nom = nom
        self.etat = False

    def show(self):
        print(self.nom)

    def __str__(self):
        return self.nom

    def change(self):
        self.etat = not(self.etat)
