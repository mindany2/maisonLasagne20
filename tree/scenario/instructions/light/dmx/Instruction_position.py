from tree.scenario.instructions.light.Instruction_light import Instruction_light
from time import sleep, time
import numpy as np
from tree.utils.Logger import Logger
RESOLUTION = 10

class Instruction_position(Instruction_light):
    """
    Change position of a lyre
    """
    def __init__(self, calculator, light, position_final, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.position_final = position_final

    def initialize(self):
        super().initialize()
        self.eval(self.position_final)

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        try:
            super().run()
            self.light.lock()
            delay = time()
 
            x_init, y_init = self.light.get_position()
            x_final, y_final = self.eval(self.position_final)
            if self.duration == 0:
                return
            nb_points = RESOLUTION*self.duration
            if x_init != x_final:
                liste_x = np.arange(x_init, x_final, (x_final-x_init)/nb_points)
            else:
                liste_x = [x_init]*int(nb_points)
            if y_init != y_final:
                liste_y = np.arange(y_init, y_final, (y_final-y_init)/nb_points)
            else:
                liste_y = [y_init]*int(nb_points)

            barrier.wait()
            for x, y in zip(liste_x, liste_y):
                temps = time()
                if self.light.test():
                    raise SystemExit("kill inst")
                self.light.set_position(int(x), int(y))
                barrier.wait()
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)

        except SystemExit:
            Logger.info("The instruction on {} was killed".format(self.light.name))

        finally:
            Logger.info("{} took {}s to move instead of {}s".format(self.light.name, time()-delay, self.duration))
            self.light.set_position(x_final, y_final)
            self.light.unlock()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : position\n")
        string += "".join("- Position : {}\n".format(self.position_final))
        return string   


