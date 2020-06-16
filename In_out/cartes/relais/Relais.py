from enum import Enum
from threading import Lock

class Etat(Enum):
    ON = 1
    OFF = 0

class Relais:
    """
    Ceci est un relais
    """
    def __init__(self):
        self.etat = Etat.OFF
        self.nombre_lumière = 0
        self.mutex = Lock()

    def set(self, etat):
        self.mutex.acquire()
        if self.nombre_lumière < 2:
            if self.etat != etat:
                self.etat = etat
                self.reload()
        self.nombre_lumière += (2*etat.value) - 1
        self.mutex.release()

    def reload(self):
        # fonction d'envoie utilisé dans les sous-classes
        pass

    def show(self):
        print( "port bus : {} | relais numero {}".format(hex(self.port_bus), self.numero))
