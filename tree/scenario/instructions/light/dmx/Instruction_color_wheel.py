from tree.scenario.instructions.light.Instruction_light import Instruction_light
from tree.connected_objects.dmx.Lyre import COLOR
from time import sleep, time
from tree.utils.Logger import Logger

class Instruction_color_wheel(Instruction_light):
    """
    Change color for a wheel (like a lyre)
    """
    def __init__(self, calculator, light, color, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.color = color

    def initialize(self):
        super().initialize()
        self.eval(self.color)

    def run(self, barrier=None):
        #There are not lock here to do not perturb the position or dimmer locker
        #It is casi-instant so no need
        super().run()
        self.light.connect()
        liste = [i.name for i in COLOR]
        self.light.set_color(COLOR[liste[self.eval(self.color)]])
        self.light.disconnect()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : color_wheel\n")
        string += "".join("- Color : {}\n".format(self.color))
        return string   


