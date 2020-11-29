from tree.scenario.instructions.Instruction import Instruction
from time import sleep, time
import numpy as np
from utils.Logger import Logger

class Instruction_strombo(Instruction):
    """
    Setup a stromboscop value to the light
    """
    def __init__(self, calculator, light, strombo, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.light = light
        self.strombo = strombo

    def run(self, barrier):
        super().run()
        barrier.wait()
        self.light.set_strombo(self.strombo)

