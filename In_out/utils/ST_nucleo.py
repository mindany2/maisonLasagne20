from enum import Enum
from time import sleep
from threading import Lock, Thread

try:
    from serial import Serial
except:
    pass

class ETAT_TRIAC(Enum):
    """
    Donne l'ordre au triac de rester allumer
    si on met une valeur impossible à atteindre
    """
    dimmer = 3
    on = 1
    off = 2


class ST_nucleo:
    """
    Carte pour les triacs
    """

    def __init__(self, addr):
        self.port = Serial(addr, baudrate=9600)
        self.mutex = Lock()
        self.addr = addr

    def set_triac(self, carte, triac, valeur, etat):
        self.mutex.acquire()
        v1 = valeur // 255 +1 
        v2 = valeur  % 255 +1
        if v1 > 255:
            v1 = 255
        if chr(v2) == "\n":
            v2 += 1
        #print("on envoie ",[chr(carte), chr(triac), chr(v1),chr(v2),chr(etat.value)])
        self.port.write([carte, triac, v1, v2, etat.value])
        #print(self.port.readline())
        sleep(0.02)
        self.mutex.release()

