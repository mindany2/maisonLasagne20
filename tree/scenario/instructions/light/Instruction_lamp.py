from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep
from tree.utils.Logger import Logger

class Instruction_lamp(Instruction_light):
    """
    Power ON or OFF a lamp
    """
    def __init__(self, calculator, light, state, delay, synchro, duration = 0):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.state = state

    def initialize(self):
        super().initialize()
        self.eval(self.state)

    def run(self, barrier):
        self.light.lock()
        super().run()
        self.state = self.eval(self.state)
        if self.light.etat() != (self.state):
            self.light.set(self.state)
        self.light.unlock()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : lamp\n")
        string += "".join("- State : {}\n".format(self.state))
        return string   


