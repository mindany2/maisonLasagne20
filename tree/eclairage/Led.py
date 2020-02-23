from tree.eclairage.Lumiere import Lumiere

class Couleur:
    """
    Permet d'avoir la couleur en rgb
    """
    def __init__(self, hexa):
        self.valeur = int(hexa,16)

    def set(self, couleur):
        self.valeur = couleur.valeur

    def __str__(self):
        return str(hex(self.valeur))

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
        print(self.nom," met le dimmeur a ",dimmeur," de couleur ",str(couleur))

    def show(self):
        print("nom = " + self.nom," | pin_addr = ",self.pin_addr, " | bluetooth_addr = ",self.bluetooth_addr, " | couleur = ", self.couleur)

