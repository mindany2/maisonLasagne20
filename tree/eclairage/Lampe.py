from tree.eclairage.Lumiere import Lumiere
from time import sleep
from threading import Lock
from In_out.cartes.Relais import Relais, Etat

class Lampe(Lumiere):
    """
    led en bluetooth
    """
    def __init__(self, nom, relais):
        Lumiere.__init__(self, nom)
        self.relais =  relais
        self.mutex = Lock()

    def set(self, on_off):
        self.mutex.acquire()
        if on_off:
            print("on allume {}".format(self.nom))
            etat = Etat.ON
        else:
            print("on eteint {}".format(self.nom))
            etat = Etat.OFF
        if self.relais.etat != etat:
            self.relais.set(etat)
        self.mutex.release()

    def show(self):
        self.relais.show()

