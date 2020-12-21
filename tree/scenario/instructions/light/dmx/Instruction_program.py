from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep, time
import numpy as np
from tree.utils.Logger import Logger

class Instruction_program(Instruction_light):
    """
    Setup a program for a dmx light
    """
    def __init__(self, calculator, light, number, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.number = number

    def initialize(self):
        super().initialize()
        self.eval(self.number)

    def run(self, barrier):
        super().run()
        barrier.wait()
        self.light.set_program(self.eval(self.number))
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : program\n")
        string += "".join("- Program : {}\n".format(self.number))
        return string   


