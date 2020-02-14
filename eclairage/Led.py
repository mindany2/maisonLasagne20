from eclairage.Lumiere import Lumiere

class Couleur:
    """
    Permet d'avoir la couleur en rgb
    """
    def __init__(this, hexa):
        this.valeur = int(hexa,16)

    def set(this, couleur):
        this.valeur = couleur.valeur

    def __str__(this):
        return str(hex(this.valeur))

class Led(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(this, nom, pin_addr, bluetooth_addr, couleur = "0x000000"):
        Lumiere.__init__(this, nom, pin_addr)
        this.couleur = Couleur(couleur)
        this.bluetooth_addr = bluetooth_addr


    def set(this, dimmeur, couleur):
        this.dimmeur = dimmeur
        # on utilise ici la sortie
        # bluetooth
        print(this.nom," met le dimmeur a ",dimmeur," de couleur ",str(couleur))

    def show(this):
        print("nom = " + this.nom," | pin_addr = ",this.pin_addr, " | bluetooth_addr = ",this.bluetooth_addr, " | couleur = ", this.couleur)

