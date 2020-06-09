from tree.eclairage.Lumiere import Lumiere
from In_out.cartes.Relais import Etat
from In_out.utils.ST_nucleo import ETAT_TRIAC
from enum import Enum
from time import sleep

class LAMPE(Enum):
    # type  = (maxi,mini)
    type_63 = (400,80)
    type_91 = (430,50)
    type_64 = (430,180)
    type_73 = (400,130)
    type_61 = (430,250)


class Projecteur(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(self, nom, triak, type_lampe, relais = None):
        Lumiere.__init__(self, nom)
        self.triak = triak
        self.relais = relais
        self.type_lampe = type_lampe
        self.dimmeur = 0
        # on eteint la lampe sur la carte
        self.triak.set(10**9,ETAT_TRIAC.off)

    def connect(self):
        print("on est connecté à "+self.nom)
        #on connect s'il faut
        if self.dimmeur == 0:
            # on met le triac en place
            self.triak.set(self.convert(0))
        elif self.dimmeur == 100:
            # on met le projo en dimmage
            self.triak.set(self.convert(100))

    def deconnect(self):
        #on deconnect s'il faut
        if self.dimmeur == 0:
            # on met la valeur max pour éteindre la lampe
            self.triak.set(10**9, ETAT_TRIAC.off)
        elif self.dimmeur == 100:
            # on met le projo à on
            self.triak.set(10**9, ETAT_TRIAC.on)
        print("on est deconnecté de "+self.nom)

    def set(self, dimmeur):
        #print("on veut set "+self.nom+" à "+str(dimmeur))
        valeur = self.convert(dimmeur)
        self.triak.set(valeur)
        self.dimmeur = int(dimmeur)

    def convert(self, dimmeur):
        # conversion du dimmeur en valeur triac
        maxi, mini = self.type_lampe.value
        valeur = int(mini + (maxi-mini)*(1-dimmeur/100))
        return valeur



    def show(self):
        print("nom = " + self.nom)

        
