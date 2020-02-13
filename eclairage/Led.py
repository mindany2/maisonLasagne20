from eclairage.Lumiere import Lumiere

def hex_to_rgb(hexa):
        red = int(hexa[2:3])
        green = int(hexa[4:5])
        blue = int(hexa[6:7])
        return [red, green, blue]

class Couleur:
    """
    Permet d'avoir la couleur en rgb
    """
    def __init__(this, hexa):
        this.couleur = hex_to_rgb(hexa)

    def set(this, couleur):
        this.couleur = couleur

    def __str__(this):
        string = ""
        for valeur in this.couleur:
            string += hex(valeur)[2::]
        return string



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
        pass

    def show(this):
        print("nom = " + this.nom," | pin_addr = ",this.pin_addr, " | bluetooth_addr = ",this.bluetooth_addr, " | couleur = ", this.couleur)

