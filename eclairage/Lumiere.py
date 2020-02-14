
class Lumiere:
    """
    Classe mère de toute les lumières
    """
    def __init__(self, nom, pin_addresse):
        self.nom = nom
        self.pin_addr = pin_addresse
        self.dimmeur = 0 #éteint
    
