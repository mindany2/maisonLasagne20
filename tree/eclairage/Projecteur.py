from tree.eclairage.Lumiere import Lumiere
from In_out.cartes.Relais import Etat
from enum import Enum
from threading import Lock

class LAMPE(Enum):
    type_plafond = 850
    type_poutre = 900

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
        self.mutex = Lock()
        # on eteint la lampe sur la carte
        self.triak.set(10**6)

    def connect(self):
        self.mutex.acquire()
        #on connect s'il faut
        if self.dimmeur == 0:
            # on met le triac en place
            self.triak.set(self.type_lampe.value)
            #on prend la main sur l'inter s'il y a
            if self.relais != None:
                self.relais.set(Etat.ON)

    def deconnect(self):
        #on deconnect s'il faut
        if self.dimmeur == 0:
            # on met la valeur max pour éteindre la lampe
            self.triak.set(10**6)
            #on prend la main sur l'inter s'il y a
            if self.relais != None:
                self.relais.set(Etat.OFF)
        self.mutex.release()

    def set(self, dimmeur):
        # conversion du dimmeur en valeur triac
        valeur_maxi = self.type_lampe.value
        valeur = int(valeur_maxi*(1-dimmeur/100))
        self.triak.set(valeur)
        self.dimmeur = int(dimmeur)


    def show(self):
        print("nom = " + self.nom)

        
