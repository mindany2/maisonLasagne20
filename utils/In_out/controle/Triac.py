from enum import Enum
from time import sleep,time
try:
    from utils.In_out.controle.Bus_spi import Bus_vers_STNucleo
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
        self.valeur = 90

    def init_valeur(self, val):
        self.set(0, 0, val)

        

    def set(self, dimmeur_final, temps, maximum):
        val = int(maximum*(1-float(dimmeur_final)/100))
        nb_points = abs(val-self.valeur)*5
        print("nb points = ",nb_points)
        compt = 0
        debut = time()
        while val != self.valeur:
            if (val > self.valeur):
                data = 1
            else:
                data = 0
            if dimmeur_final == 0:
                data = 1
            else:
                data = 0
            print("data = ", data)
            print("on veut ",self.valeur ," == ", val)
            (valeur,etat) = Bus_vers_STNucleo().write(self.numero_carte-1, self.numero_triak-1, data)
            print("la valeur reçu est de {}".format(valeur))
            if (self.valeur == valeur):
                compt += 1
            else:
                compt = 0
            if compt > 30:
                break
            self.valeur = valeur
            sleep(1/nb_points*temps)
        print("on a mit {} s, au lieu de {} s".format(time()-debut, temps))
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
