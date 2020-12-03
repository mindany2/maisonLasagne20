from tree.scenario.instructions.Instruction import Instruction
from time import sleep, time
import numpy as np
from tree.utils.Logger import Logger

class Instruction_speed(Instruction):
    """
    Setup the speed of a dmx light (mouvement, patern_speed..)
    """
    def __init__(self, calculator, light, value, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.light = light
        self.value = value

    def run(self, barrier):
        super().run()
        barrier.wait()
        self.light.set_speed(self.eval(self.value))
