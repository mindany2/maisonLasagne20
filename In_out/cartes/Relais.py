from enum import Enum
from In_out.utils.Port_extender import Port_extender
from threading import Lock

class Etat(Enum):
    ON = 1
    OFF = 0

class Relais:
    """
    Ceci est un relais
    """
    def __init__(self, port_bus, registre, numero):
        self.port_bus = port_bus
        self.numero = numero
        self.registre = registre
        self.etat = Etat.OFF
        self.nombre_lumière = 0
        self.mutex = Lock()

    def set(self, etat):
        self.mutex.acquire()
        if self.nombre_lumière < 2:
            if self.etat != etat:
                self.etat = etat
                print("on do etat = {}".format(etat))
                Port_extender().write_pin(self.port_bus, self.registre, self.numero, self.etat.value)
        self.nombre_lumière += (2*etat.value) - 1
        print("nombre_lumière = {}".format(self.nombre_lumière))
        self.mutex.release()



    def show(self):
        print( "port bus : {} | relais numero {}".format(hex(self.port_bus), self.numero))
