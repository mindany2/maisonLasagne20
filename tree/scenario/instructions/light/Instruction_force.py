from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep
from tree.utils.Logger import Logger

class Instruction_force(Instruction_light):
    """
    Force a relay of a lamp to be always ON 
    """
    def __init__(self, calculator, light, state, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.state = state

    def initialize(self):
        super().initialize()
        self.eval(self.state)

    def run(self, barrier=None):
        self.light.lock()
        super().run()
        self.state = self.eval(self.state)
        self.light.force_relay(self.state)
        self.light.unlock()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : force\n")
        string += "".join("- State : {}\n".format(self.state))
        return string   


