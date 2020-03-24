from enum import Enum
from time import sleep
try:
    from utils.controle.Bus_spi import Bus_vers_STNucleo
except:
    from Bus_spi import Bus_vers_STNucleo

class ETAT(Enum):
    EN_COURS = 2
    ON = 1
    OFF = 0

FACTEUR = 85

class Triac:
    """
    Ceci est un triac
    """
    def __init__(self, numero_carte, numero_triak):
        self.numero_carte = numero_carte
        self.numero_triak = numero_triak
        (valeur,self.etat) = Bus_vers_STNucleo().write(numero_carte, numero_triak,0)
        self.valeur = valeur

    def set(self, dimmeur):
        val = FACTEUR-int((float(dimmeur)/100)*FACTEUR)
        count = 0
        while self.valeur != val:
            data = 2*(val < self.valeur) + 3*(val > self.valeur)
            print("data = ", data)
            print("on veut ",self.valeur ," == ", val)
            (valeur,etat) = Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, data)
            print(dimmeur)
            if self.valeur == valeur:
                count += 1
            else:
                count = 0
            self.valeur = valeur
            sleep(0.02)
        return 0


    def connect(self):
        while self.etat == 0:
            (valeur, etat) = Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, 1)
            self.etat = etat

    def deconnect(self):
        while self.etat == 1:
            (valeur, etat) = Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, 0)
            self.etat = etat

    def show(self):
        print( "carte numéro : {} | triac numéro {}".format(self.numero_carte, self.numero_triak))


if __name__ == "__main__":
    pass
