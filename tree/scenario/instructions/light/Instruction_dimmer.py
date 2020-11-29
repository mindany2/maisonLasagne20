from tree.scenario.instructions.light.Instruction_light import Instruction_light, RESOLUTION
from time import sleep, time
from utils.Logger import Logger

class Instruction_dimmer(Instruction_light):
    """
    Dim a light
    """
    def __init__(self, calculator, light, dimmer, duration, delay, synchro):
        Instruction_light.__init__(self, calculator, light, dimmer, duration, delay, synchro)

    def run(self, barrier):
        """
        Setup a try/finally to allow kill from another instruction
        """
        try:
            self.light.lock()
            delay = time()
            dimmer_initial = self.light.dimmer
            dimmer_final = self.eval(self.dimmer)
            gap = dimmer_final - dimmer_initial
            nb_dots = self.eval(self.duration)*RESOLUTION

            if dimmer_initial == dimmer_final:
                return

            self.light.connect()
            super().run(time_spent=(time()-delay))
            if gap != 0 and self.duration == 0:
                self.light.set(dimmer_final)
                return
            barrier.wait()
            val = dimmer_initial
            debut = time()
            for _ in range(0,nb_dots):
                if self.light.test():
                    raise SystemExit("kill inst")
                temps = time()
                self.light.set(val)
                val += gap/nb_dots
                dodo = 1/RESOLUTION-(time()-temps)
                if dodo > 0:
                    sleep(dodo)
            self.light.set(dimmer_final)
            Logger.info(" the light {} took {}s to power instead of {}s".format(self.light.name, time()-debut, self.duration))

        finally:
            self.light.disconnect()
            self.light.unlock()

    def show(self):
        print("projo = ",self.light.name, " | dimmer = ", self.dimmer, " | duration = ", self.duration)
