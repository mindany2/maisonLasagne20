from tree.scenario.instructions.Instruction import Instruction, STATE

RESOLUTION = 10

class Instruction_light(Instruction):
    """
    Instruction with a value and a light
    """
    def __init__(self, calculator, light, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.light = light

    def __eq__(self, other):
        if isinstance(other, Instruction_light):
            return (self.light == other.light) 
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Light : {}\n".format(self.light.name))
        return string
