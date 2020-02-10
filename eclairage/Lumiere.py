
class Lumiere:
    """
    Classe mère de toute les lumières
    """
    def __init__(this, nom, pin_addresse):
        this.nom = nom
        this.pin_addr = pin_addresse
        this.dimmeur = 0 #éteint
    
