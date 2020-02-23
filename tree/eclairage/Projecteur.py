from tree.eclairage.Lumiere import Lumiere

class Projecteur(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(self, nom, pin_addr):
        Lumiere.__init__(self, nom, pin_addr)


    def set(self, dimmeur):
        self.dimmeur = dimmeur
        # on utilise ici la sortie
        #du raspberry
        print(self.nom," met le dimmeur a ",dimmeur)

    def show(self):
        print("nom = " + self.nom," | pin_addr = ",self.pin_addr)
        
