from tree.scenario.instructions.Instruction import Instruction
from tree.utils.Logger import Logger
import os

class Instruction_command(Instruction):
    """
    Instruction for starting a bash command
    """
    def __init__(self,calculator, command, delay, condition, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.command = command
        self.condition = condition

    def run(self, barrier=None):
        super().run()
        if self.eval(self.condition):
            os.system(self.command)
        #Logger.debug("set the variable {} to {}".format(self.variable.name, self.variable.get()))

    def __str__(self):
        string = super().__str__()
        string += "".join("- Command : {}\n".format(self.command))
        return string
