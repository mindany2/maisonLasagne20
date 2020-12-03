from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep
from tree.utils.Logger import Logger

class Instruction_lamp(Instruction_light):
    """
    Power ON or OFF a lamp
    """
    def __init__(self, calculator, light, dimmer, delay, synchro, duration = 0):
        Instruction_light.__init__(self, calculator, light, dimmer, duration, delay, synchro)

    def run(self, barrier):
        self.light.lock()
        super().run()
        self.dimmer = self.eval(self.dimmer)
        if self.light.etat() != (self.dimmer != 0):
            self.light.set(self.dimmer != 0)
        self.light.unlock()
