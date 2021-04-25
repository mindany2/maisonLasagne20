from tree.scenario.instructions.Instruction import Instruction
from tree.utils.Logger import Logger

class Instruction_mode(Instruction):
    """
    Instruction for changing the actual mode
    """
    def __init__(self,calculator, tree, name_mode, delay, condition, synchro, duration = 0):
        Instruction.__init__(self,calculator, duration, delay, synchro)
        self.tree = tree
        self.name_mode = name_mode
        self.condition = condition

    def run(self, barrier=None):
        super().run()
        if self.eval(self.condition):
            self.tree.change_mode(self.name_mode)
        #Logger.debug("set the variable {} to {}".format(self.variable.name, self.variable.get()))

    def initialize(self):
        super().initialize()

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : mode\n")
        string += "".join("- Mode : {}\n".format(self.name_mode))
        return string
