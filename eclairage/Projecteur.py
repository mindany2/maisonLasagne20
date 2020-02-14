from eclairage.Lumiere import Lumiere

class Projecteur(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(this, nom, pin_addr):
        Lumiere.__init__(this, nom, pin_addr)


    def set(this, dimmeur):
        this.dimmeur = dimmeur
        # on utilise ici la sortie
        #du raspberry
        print(this.nom," met le dimmeur a ",dimmeur)

    def show(this):
        print("nom = " + this.nom," | pin_addr = ",this.pin_addr)
        
