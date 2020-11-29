from tree.scenario.instructions.Instruction import Instruction
from tree.connected_objects.dmx.Lyre import COLOR
from time import sleep, time
from utils.Logger import Logger

class Instruction_color_wheel(Instruction):
    """
    Change color for a wheel (like a lyre)
    """
    def __init__(self, calculator, light, color, duration, delay, synchro):
        Instruction.__init__(self, calculator, duration, delay, synchro)
        self.light = light
        self.color = color

    def run(self, barrier):
        super().run()
        barrier.wait()
        liste = [i.name for i in COLOR]
        self.light.set_color(COLOR[liste[self.eval(self.color)]])
