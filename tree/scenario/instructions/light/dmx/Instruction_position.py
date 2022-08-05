from tree.scenario.instructions.light.Instruction_light import Instruction_light
import time
import numpy as np
from tree.utils.Logger import Logger
RESOLUTION = 10

class Instruction_position(Instruction_light):
    """
    Change position of a lyre
    """
    def __init__(self, calculator, light, x, y, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.x, self.y = x, y

    def initialize(self):
        super().initialize()
        self.eval(self.x)
        self.eval(self.y)

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        try:
            self.light.lock_position()
            super().run()
 
            x_init, y_init = self.light.get_position()
            x_final, y_final = self.eval(self.x), self.eval(self.y)
            if self.duration == 0:
                self.light.set_position(x_final, y_final)
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
                temps = time.time()
                assert not self.light.test_position()
                self.light.set_position(int(x), int(y))
                barrier.wait()
                dodo = 1/RESOLUTION-(time.time()-temps)
                if dodo > 0:
                    time.sleep(dodo)
            self.light.set_position(x_final, y_final)

        except AssertionError:
            # the inst is killed
            Logger.info("The instruction on {} was killed".format(self.light.name))

        finally:
            #Logger.info("{} took {}s to move instead of {}s".format(self.light.name, time()-delay, self.duration))
            self.light.unlock_position()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : position\n")
        string += "".join("- Position : {},{}\n".format(self.x, self.y))
        return string   


