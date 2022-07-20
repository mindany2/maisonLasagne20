from tree.scenario.instructions.Instruction import Instruction
from tree.utils.Logger import Logger
import time

RESOLUTION = 10

class Instruction_speaker(Instruction):
    """
    Change de volume of speakers
    """
    def __init__(self, calculator, speaker, volume, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.volume = volume
        self.speaker = speaker

    def initialize(self):
        super().initialize()
        self.eval(self.volume)

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        try:
            self.speaker.lock()
            super().run()

            volume_initial = self.speaker.volume()
            volume_final = self.eval(self.volume)
            gap = volume_final - volume_initial

            if gap == 0:
                return

            nb_dots = self.duration*RESOLUTION
            if not self.speaker.connect():
                return
            assert not self.speaker.test()

            val = volume_initial
            for _ in range(0,nb_dots):
                assert not self.speaker.test()
                temps = time.time()
                self.speaker.change_volume(int(val))
                val += gap/nb_dots
                dodo = 1/RESOLUTION-(time.time()-temps)
                if dodo > 0:
                    time.sleep(dodo)
            self.speaker.change_volume(volume_final)
            self.speaker.disconnect()
        except AssertionError:
            # the inst was killed
            pass
        finally:
            self.speaker.unlock()
  
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : speaker\n")
        string += "".join("- Speakers : {}\n".format(self.speaker.name))
        string += "".join("- Volume : {}\n".format(self.volume))
        return string   




