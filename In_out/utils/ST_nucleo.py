from In_out.utils.I2C import I2C
from enum import Enum
from time import sleep
from threading import Lock

class ETAT_TRIAC(Enum):
    """
    Donne l'ordre au triac de rester allumer
    si on met une valeur impossible à atteindre
    """
    dimmer = 0
    on = 1
    off = 2

class ST_nucleo:
    """
    Carte pour les triacs
    """

    i2c = I2C()
    ip = 0x10
    mutex = Lock()

    @classmethod
    def set(self, carte, triac, valeur, etat):
        self.mutex.acquire()
        v1 = valeur // 255
        v2 = valeur  % 255
        self.i2c.write_data(self.ip, [carte, triac, v1, v2, etat.value])
        sleep(0.0004)
        self.mutex.release()
