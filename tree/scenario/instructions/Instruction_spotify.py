from tree.scenario.instructions.Instruction import Instruction
from tree.utils.Logger import Logger
from enum import Enum

class TYPE_INST_SPOTIFY(Enum):
    start = 0
    stop = 1
    volume = 2
    next_track = 3
    start_playlist = 4

class Instruction_spotify(Instruction):
    """
    Modifie spotify values like volumes, play/pause..
    """
    def __init__(self,calculator, spotify, type_inst, val, delay, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.type_inst = type_inst
        self.spotify = spotify
        self.val = val

    def run(self, barrier=None):
        super().run()
        Logger.info(f"{self.type_inst} spotify")
        if self.type_inst == TYPE_INST_SPOTIFY.start:
            self.spotify.start()
        elif self.type_inst == TYPE_INST_SPOTIFY.stop:
            self.spotify.kill()
        elif self.type_inst == TYPE_INST_SPOTIFY.volume:
            self.spotify.set_volume(self.eval(self.val))
        elif self.type_inst == TYPE_INST_SPOTIFY.start_playlist:
            self.spotify.start(context_uri=str(self.val))
        elif self.type_inst == TYPE_INST_SPOTIFY.next_track:
            self.spotify.next_track()

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : spotify\n")
        string += "".join("- Action : {}\n".format(self.type_inst))
        string += "".join("- Args : {}\n".format(self.val))
        return string
