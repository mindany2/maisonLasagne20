from tree.scenario.instructions.Instruction import Instruction, STATE

RESOLUTION = 10

class Instruction_light(Instruction):
    """
    Instruction with a dimmer and a light
    """
    def __init__(self, calculator, light, dimmer, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.dimmer = dimmer
        self.light = light

    def __eq__(self, other):
        if isinstance(other, Instruction_light):
            return (self.dimmer == other.dimmer) and (self.light == other.light) 
        return False
