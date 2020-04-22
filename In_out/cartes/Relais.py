from enum import Enum
from In_out.utils.Port_extender import Port_extender

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
        self.etat = None
        self.nombre_lumière = 0

    def set(self, etat):
        self.etat = etat
        self.nombre_lumière -= (1-etat.value)
        if self.nombre_lumière == 0:
            Port_extender().write_pin(self.port_bus, self.registre, self.numero, self.etat.value)
        self.nombre_lumière += etat.value



    def show(self):
        print( "port bus : {} | relais numero {}".format(hex(self.port_bus), self.numero))
