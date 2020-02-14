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
    def __init__(self, hexa):
        self.couleur = hex_to_rgb(hexa)

    def set(self, couleur):
        self.couleur = couleur

    def __str__(self):
        string = ""
        for valeur in self.couleur:
            string += hex(valeur)[2::]
        return string



class Led(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(self, nom, pin_addr, bluetooth_addr, couleur = "0x000000"):
        Lumiere.__init__(self, nom, pin_addr)
        self.couleur = Couleur(couleur)
        self.bluetooth_addr = bluetooth_addr


    def set(self, dimmeur, couleur):
        self.dimmeur = dimmeur
        # on utilise ici la sortie
        # bluetooth
        pass

    def show(self):
        print("nom = " + self.nom," | pin_addr = ",self.pin_addr, " | bluetooth_addr = ",self.bluetooth_addr, " | couleur = ", self.couleur)

