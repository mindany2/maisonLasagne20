from enum import Enum
from threading import Thread

class Attente(Enum):
    CONTINUE = 0
    WAIT = 1


class Instruction(Thread):
    """
    Juste une class qui est vide pour
    être la parentes de bluetooth et pin
    """
    def __init__(self, duree, attente):
        Thread.__init__(self)
        self.attente = attente
        self.duree = duree

    def run(self):
        # implémenter dans les sous-classes
        pass
