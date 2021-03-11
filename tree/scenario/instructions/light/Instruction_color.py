import numpy as np
from tree.scenario.instructions.light.Instruction_light import Instruction_light, RESOLUTION
from tree.utils.Color import Color
from time import sleep,time
from tree.utils.Logger import Logger

class Instruction_color(Instruction_light):
    """
    Instruction for a RBG colors light
    """
    def __init__(self, calculator, light, dimmer, duration, delay, synchro, color):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.color = color
        self.dimmer = dimmer

    def initialize(self):
        super().initialize()
        self.eval(self.color)
        self.eval(self.dimmer)

    def run(self, barrier):
        delay = time()
        
        try:
            self.light.lock()
            dimmer_final = self.eval(self.dimmer)
            dimmer_initial = self.light.dimmer
            color = Color(self.eval(self.color))
            Logger.debug("Set led {} to {}".format(self.light.name, color))
            if self.eval(self.duration) == 0:
                if dimmer_final != dimmer_initial or color != self.light.color:
                    if self.light.connect():
                        super().run(time_spent=(time()-delay))
                        self.light.set_color(dimmer_final, color.value)
                        self.light.disconnect()
                return

            nb_dots = RESOLUTION*self.eval(self.duration)
            if dimmer_initial != dimmer_final:
                liste_dimmer = np.arange(dimmer_initial, dimmer_final, (dimmer_final-dimmer_initial)/nb_dots)
            else:
                liste_dimmer = [dimmer_initial]*nb_dots
            if color != self.light.color:
                liste_color = color.generate_array(self.light.color, nb_dots)
            else:
                barrier.wait()
                self.light.disconnect()
                return

            if self.light.test():
                raise SystemExit("kill inst")

            connected = self.light.connect()
            if not(connected):
                barrier.wait()
                return
            super().run(time_spent=(time()-delay))

            barrier.wait()
            for dim, value_color in zip(liste_dimmer, liste_color):
                if self.light.test():
                    raise SystemExit("kill inst")
                self.light.set_color(dim, value_color)
                sleep(1/RESOLUTION)
                barrier.wait()
            self.light.set_color(dimmer_final, color.value)
            self.light.disconnect()

        finally:
            self.light.unlock()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : color\n")
        string += "".join("- Color : {}\n".format(self.color))
        string += "".join("- Dimmer : {}\n".format(self.dimmer))
        return string   


