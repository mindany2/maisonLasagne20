from eclairage.Lumiere import Lumiere

class Couleur:
    """
    Permet d'avoir la couleur en rgb
    """
    def __init__(this):
        this.couleur = [0, 0, 0]

    def set(this, couleur):
        this.couleur = couleur

    def __str__(this):
        string = ""
        for valeur in this.couleur:
            string += hex(valeur)[2::]
        print(string)
        return string


class Led(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(this, nom, pin_addr):
        Lumiere.__init__(nom, pin_addr)
        this.couleur = "000000"


    def set(this, dimmeur):
        this.dimmeur = dimmeur
        # on utilise ici la sortie
        # bluetooth
        pass

