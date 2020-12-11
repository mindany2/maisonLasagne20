from tree.scenario.instructions.light.Instruction_light import Instruction_light
from tree.connected_objects.dmx.Lyre import GOBO
from time import sleep, time
from tree.utils.Logger import Logger

class Instruction_gobo(Instruction_light):
    """
    Change Gobo on lyre
    """
    def __init__(self, calculator,light, gobo, duration, temps_init, synchro):
        Instruction_light.__init__(self, calculator, light, duration, temps_init, synchro)
        self.gobo = gobo

    def initialize(self):
        super().initialize()
        self.eval(self.gobo)

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        super().run(time_spent=0)
        barrier.wait()
        liste = [i.name for i in GOBO]
        self.light.set_gobo(GOBO[liste[self.eval(self.gobo)]])
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : gobo\n")
        string += "".join("- Gobo : {}\n".format(self.gobo))
        return string   


