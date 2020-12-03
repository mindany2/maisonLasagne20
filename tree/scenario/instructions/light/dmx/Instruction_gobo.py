from tree.scenario.instructions.Instruction import Instruction
from tree.connected_objects.dmx.Lyre import GOBO
from time import sleep, time
from tree.utils.Logger import Logger

class Instruction_gobo(Instruction):
    """
    Change Gobo on lyre
    """
    def __init__(self, calculator,light, gobo, duration, temps_init, synchro):
        Instruction.__init__(self, calculator, duration, temps_init, synchro)
        self.light = light
        self.gobo = gobo

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        super().run(time_spent=0)
        barrier.wait()
        liste = [i.name for i in GOBO]
        self.light.set_gobo(GOBO[liste[self.eval(self.gobo)]])
