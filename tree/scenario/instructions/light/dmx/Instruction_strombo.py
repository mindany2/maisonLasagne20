from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep, time
import numpy as np
from tree.utils.Logger import Logger

class Instruction_strombo(Instruction_light):
    """
    Setup a stromboscop value to the light
    """
    def __init__(self, calculator, light, strombo, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.strombo = strombo

    def initialize(self):
        super().initialize()
        self.eval(self.strombo)

    def run(self, barrier=None):
        super().run()
        self.light.set_strombo(self.eval(self.strombo))
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : strombo\n")
        string += "".join("- Value : {}\n".format(self.strombo))
        return string   


