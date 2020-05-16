from enum import Enum
from time import sleep,time
from In_out.utils.ST_nucleo import ST_nucleo, ETAT_TRIAC

class Triac:
    """
    Ceci est un triac
    """
    def __init__(self, numero_carte, numero_triak):
        self.numero_carte = numero_carte
        self.numero_triak = numero_triak
        self.valeur = 99999

    def set(self, valeur, etat=ETAT_TRIAC.dimmer):
        if self.valeur != valeur:
            ST_nucleo().set(self.numero_carte, self.numero_triak, valeur, etat)
            self.valeur = valeur


    def show(self):
        print( "carte numéro : {} | triac numéro {}".format(self.numero_carte, self.numero_triak))


if __name__ == "__main__":
    pass
