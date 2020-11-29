from tree.scenario.instructions.Instruction import Instruction
from time import sleep, time
import numpy as np
from utils.Logger import Logger

class Instruction_program(Instruction):
    """
    Setup a program for a dmx light
    """
    def __init__(self, calculator, light, numero, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.light = light
        self.numero = numero

    def run(self, barrier):
        super().run()
        barrier.wait()
        self.light.set_program(self.eval(self.numero))
