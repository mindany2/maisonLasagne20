import numpy as np
from tree.scenario.Instruction import Instruction
from utils.spotify.Spotify import Spotify
from time import sleep
from utils.Logger import Logger
from enum import Enum
from random import randint

class TYPE_INST_SPOTIFY(Enum):
    start = 0
    stop = 1

class Instruction_spotify(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, type_inst, temps_init, synchro, duree = 0):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.type_inst = type_inst

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run()
        if self.type_inst == TYPE_INST_SPOTIFY.start:
            Spotify().start()
        elif self.type_inst == TYPE_INST_SPOTIFY.stop:
            Spotify().kill()
