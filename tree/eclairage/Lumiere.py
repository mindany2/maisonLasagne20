from tree.utils.Locker import Locker

class Lumiere(Locker):
    """
    Classe mère de toute les lumières
    """
    def __init__(self, nom):
        Locker.__init__(self)
        self.nom = nom
        self.dimmeur = 0 #éteint
        
