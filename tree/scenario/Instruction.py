from enum import Enum
from time import sleep
from threading import Thread, Barrier
from utils.spotify.Spotify import Spotify

class Attente(Enum):
    CONTINUE = 0
    WAIT = 1

class Instruction():
    """
    Juste une class qui est vide pour
    être la parentes de bluetooth et pin
    """
    def __init__(self, duree, temps_init, synchro):
        self.temps_init = temps_init
        self.duree = duree
        self.synchro = synchro

    def run(self, temps_ecouler = 0):
        if self.temps_init.count("bpm") == 0:
            if temps_ecouler < int(self.temps_init):
                sleep(int(self.temps_init)-temps_ecouler)
        else:
            # on doit attendre le bpm
            numero = int(self.temps_init.split("_")[1])
            Spotify.wait_for_beat(numero)
        # le reste est dans les sous-classes


    def eclairage(self):
        return None

