import numpy as np
from tree.scenario.instructions.Instruction import Instruction
from In_out.spotify.Spotify import Spotify
from time import sleep
from tree.utils.Logger import Logger
from enum import Enum
from random import randint

class TYPE_INST_SPOTIFY(Enum):
    start = 0
    stop = 1

class Instruction_spotify(Instruction):
    """
    Modifie spotify values like volumes, play/pause..
    """
    #TODO volume
    def __init__(self,calculator, type_inst, delay, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.type_inst = type_inst

    def run(self, barrier):
        super().run()
        if self.type_inst == TYPE_INST_SPOTIFY.start:
            Spotify().start()
        elif self.type_inst == TYPE_INST_SPOTIFY.stop:
            Spotify().kill()
