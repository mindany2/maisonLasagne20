from tree.scenario.instructions.Instruction import Instruction
from time import sleep
from tree.utils.Logger import Logger
from enum import Enum
from random import randint

class TYPE_INST_VAR(Enum):
    init = 0
    random = 1

class Instruction_variable(Instruction):
    """
    Set a variable to a value
    """
    def __init__(self,calculator, variable, type_inst, value, delay, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.variable = variable
        self.type_inst = type_inst
        self.value = value

    def run(self, barrier):
        super().run()
        if self.type_inst == TYPE_INST_VAR.init:
            self.variable.set(self.eval(self.value))
        elif self.type_inst == TYPE_INST_VAR.random:
            val = self.eval(self.value)
            self.variable.set(randint(val[0], val[1]))
        Logger.debug("set the variable {} to {}".format(self.variable.name, self.variable.get()))

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : variable\n")
        string += "".join("- Action : {}\n".format(self.type_inst))
        string += "".join("- Variable : {}\n".format(self.variable.name))
        string += "".join("- Value : {}\n".format(self.value))
        return string
