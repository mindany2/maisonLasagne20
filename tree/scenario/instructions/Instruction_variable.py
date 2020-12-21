from tree.scenario.instructions.Instruction import Instruction
from time import sleep
from tree.utils.Logger import Logger
from enum import Enum
from random import randint

class Instruction_variable(Instruction):
    """
    Set a variable to a value
    """
    def __init__(self,calculator, variable, value, delay, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.variable = variable
        self.value = value

    def run(self, barrier):
        super().run()
        self.variable.set(self.eval(self.value))
        #Logger.debug("set the variable {} to {}".format(self.variable.name, self.variable.get()))

    def initialize(self):
        super().initialize()
        self.eval(self.value)

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : variable\n")
        string += "".join("- Variable : {}\n".format(self.variable.name))
        string += "".join("- Value : {}\n".format(self.value))
        return string
