from tree.scenario.instructions.light.Instruction_light import Instruction_light, RESOLUTION
import time
from tree.utils.Logger import Logger

class Instruction_dimmer(Instruction_light):
    """
    Dim a light
    """
    def __init__(self, calculator, light, dimmer, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, duration, delay, synchro)
        self.dimmer = dimmer

    def initialize(self):
        super().initialize()
        self.eval(self.dimmer)

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        try:
            self.light.lock()
            delay = time.time()
            dimmer_initial = self.light.dimmer
            dimmer_final = self.eval(self.dimmer)
            gap = dimmer_final - dimmer_initial
            nb_dots = self.eval(self.duration)*RESOLUTION

            if dimmer_initial == dimmer_final:
                return

            if not self.light.connect():
                barrier.wait()
                return
            super().run(time_spent=(time.time()-delay))
            assert not self.light.test()
            if self.duration == 0:
                self.light.set_dimmer(dimmer_final)
                self.light.disconnect()
                return
            barrier.wait()
            val = dimmer_initial
            debut = time.time()
            for _ in range(0,nb_dots):
                assert not self.light.test()
                temps = time.time()
                self.light.set_dimmer(val)
                val += gap/nb_dots
                dodo = 1/RESOLUTION-(time.time()-temps)
                if dodo > 0:
                    time.sleep(dodo)
            self.light.set_dimmer(dimmer_final)
            self.light.disconnect()
        except AssertionError:
            #The inst what killed
            pass

        finally:
            self.light.unlock()
 
    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : dimmer\n")
        string += "".join("- Dimmer : {}\n".format(self.dimmer))
        return string   


