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
    def __init__(this, attente = Attente.CONTINUE):
        Thread.__init__(this)
        this.attente = attente

    def run(this):
        # implémenter dans les sous-classes
        pass
