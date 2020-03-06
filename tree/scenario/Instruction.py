from enum import Enum
from threading import Thread, Barrier

class Attente(Enum):
    CONTINUE = 0
    WAIT = 1


class Instruction():
    """
    Juste une class qui est vide pour
    être la parentes de bluetooth et pin
    """
    def __init__(self, duree, attente):
        self.attente = attente
        self.duree = duree

    def run(self, barrier):
        # implémenter dans les sous-classes
        pass
