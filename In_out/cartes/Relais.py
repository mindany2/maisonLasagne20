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
        self.etat = Etat.OFF
        self.nombre_lumière = 0

    def set(self, etat):
        print(etat, self.etat)
        if self.etat != etat:
            print("nombre_lumière {}".format(self.nombre_lumière))
            if self.nombre_lumière < 2:
                self.etat = etat
                Port_extender().write_pin(self.port_bus, self.registre, self.numero, self.etat.value)
        self.nombre_lumière += 2*etat.value - 1



    def show(self):
        print( "port bus : {} | relais numero {}".format(hex(self.port_bus), self.numero))
