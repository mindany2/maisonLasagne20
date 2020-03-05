from tree.eclairage.Lumiere import Lumiere

class Projecteur(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(self, nom, triak):
        Lumiere.__init__(self, nom)
        self.triak = triak


    """
    def connect(self):
        self.triak.
    """
    def set(self, dimmeur):
        self.dimmeur = dimmeur
        # on utilise ici la sortie
        #du raspberry
        print(self.nom," met le dimmeur a ",dimmeur)

    def show(self):
        print("nom = " + self.nom)
        self.triak.show()

        
