from tree.scenario.instructions.Instruction import Instruction
from tree.utils.Logger import Logger
from enum import Enum

class TYPE_INST_SPOTIFY(Enum):
    start = 0
    stop = 1

class Instruction_spotify(Instruction):
    """
    Modifie spotify values like volumes, play/pause..
    """
    #TODO volume
    def __init__(self,calculator, spotify, type_inst, delay, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.type_inst = type_inst
        self.spotify = spotify

    def run(self, barrier):
        super().run()
        if self.type_inst == TYPE_INST_SPOTIFY.start:
            self.spotify.start()
        elif self.type_inst == TYPE_INST_SPOTIFY.stop:
            self.spotify.kill()

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : spotify\n")
        string += "".join("- Action : {}\n".format(self.type_inst))
        return string
