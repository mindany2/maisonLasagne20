from enum import Enum

class ETAT(Enum):
    ON = 0
    OFF = 1
    EN_COURS = 2

class Triac:
    """
    Ceci est un triac
    """
    def __init__(self, port_bus, registre, numero):
        self.port_bus = port_bus
        self.numero = numero
        self.registre = registre
        self.etat = ETAT.OFF
        self.time_sleep = 0

    def set_etat(self):
        pass

    def show(self):
        print( "port bus : {} | relais numéro {}".format(self.port_bus, self.numero))
