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
        self.id_liste = 0
        self.calculateur = None

    def run(self, temps_ecouler = 0):
        self.duree=self.eval(self.duree)
        if self.temps_init.count("bpm") == 0:
            if temps_ecouler < self.eval(self.temps_init):
                sleep(self.calculateur.eval(self.temps_init)-temps_ecouler)
        else:
            # on doit attendre le bpm
            numero = self.calculateur.eval(self.temps_init.split("_")[1])
            Spotify.wait_for_beat(numero)
            if self.temps_init.count(","):
                # on doit attendre en plus
                sleep(self.eval(self.temps_init.split(",")[0]))

        # le reste est dans les sous-classes

    def finish(self):
        pass

    def eval(self, string):
        if self.calculateur:
            return self.calculateur.eval(string)
        return int(string)

    def eclairage(self):
        return None

