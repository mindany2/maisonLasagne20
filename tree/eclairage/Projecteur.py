from tree.eclairage.Lumiere import Lumiere
from utils.In_out.controle.Relais import Etat
from enum import Enum

class LAMPE(Enum):
    type_plafond = 85
    type_poutre = 90

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
        #self.triak.init_valeur(type_lampe.value)

    def connect(self):
        #on prend la main sur l'inter s'il y a
        if self.relais != None:
            #on connect s'il faut
            if self.dimmeur == 0:
                self.relais.set(Etat.ON)

    def deconnect(self):
        #on prend la main sur l'inter s'il y a
        if self.relais != None:
            #on deconnect s'il faut
            if self.dimmeur == 0:
                self.relais.set(Etat.OFF)

    def set(self, dimmeur, temps):
        self.dimmeur = dimmeur
        self.triak.set(dimmeur, temps, self.type_lampe.value)


    def show(self):
        print("nom = " + self.nom)

        
