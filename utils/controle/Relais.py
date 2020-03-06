from enum import Enum
from commande.Bus import Bus

class Etat(Enum):
    ON = 0
    OFF = 1

class Relais:
    """
    Ceci est un relais
    """
    def __init__(self, port_bus, registre, numero):
        self.port_bus = port_bus
        self.numero = numero
        self.registre = registre
        self.etat = None

    def set(self, etat):
        self.etat = etat
        Bus().write_pin(self.port_bus, self.registre, self.numero, self.etat.value)



    def show(self):
        print( "port bus : {} | relais numero {}".format(hex(self.port_bus), self.numero))
