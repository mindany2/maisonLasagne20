from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep, time
import numpy as np
from tree.utils.Logger import Logger

class Instruction_speed(Instruction_light):
    """
    Setup the speed of a dmx light (mouvement, patern_speed..)
    """
    def __init__(self, calculator, light, value, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.value = value

    def initialize(self):
        super().initialize()
        self.eval(self.value)

    def run(self, barrier=None):
        super().run()
        self.light.connect()
        self.light.set_speed(self.eval(self.value))
        self.light.disconnect()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : speed\n")
        string += "".join("- Speed : {}\n".format(self.value))
        return string   


