import numpy as np
from tree.scenario.Instruction import Instruction
from time import sleep
from utils.Logger import Logger
from enum import Enum
from random import randint

class TYPE_INST(Enum):
    init = 0
    random = 1

class Instruction_variable(Instruction):
    """
    On set un projecteur
    """
    def __init__(self, variable, type_inst, value, temps_init, synchro, duree = 0):
        Instruction.__init__(self, duree, temps_init, synchro)
        self.variable = variable
        self.type_inst = type_inst
        self.value = value

    def run(self, barrier):
        """
        On s'occupe de faire l'instruction
        """
        super().run()
        if self.type_inst == TYPE_INST.init:
            self.variable.set(self.eval(self.value))
        elif self.type_inst == TYPE_INST.random:
            val = self.eval(self.value)
            self.variable.set(randint(val[0], val[1]))

        Logger.debug("on met la variable {} a {}".format(self.variable.nom, self.variable.get()))
