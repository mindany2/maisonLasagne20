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
        val = 85-int((float(dimmeur)/100)*85)
        data = 2*(val < self.valeur) + 3*(val > self.valeur)
        while self.valeur != val:
            print("on veut ",self.valeur ," == ", val)
            (valeur,etat) = Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, data)
            print(dimmeur)
            self.valeur = valeur
            sleep(0.01)


    def connect(self):
        Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, 1)

    def deconnect(self):
        Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, 0)

    def show(self):
        print( "carte numéro : {} | triac numéro {}".format(self.numero_carte, self.numero_triak))


if __name__ == "__main__":
    pass
