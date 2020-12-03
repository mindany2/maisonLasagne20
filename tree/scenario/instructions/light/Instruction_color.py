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
        Instruction_light.__init__(self, calculator, light, dimmer, duration, delay, synchro)
        self.color = color

    def run(self, barrier):
        delay = time()
        err, err1 = False, False
        
        try:
            self.light.lock()
            dimmer_final = self.eval(self.dimmer)
            dimmer_initial = self.light.dimmer
            color = Color(self.eval(self.color))
            if self.eval(self.duration) == 0:
                super().run(time_spent=(time()-delay))
                self.light.connect()
                self.light.set_color(dimmer_final, color.value)
                return

            nb_dots = RESOLUTION*self.eval(self.duration)
            if dimmer_initial != dimmer_final:
                liste_dimmer = np.arange(dimmer_initial, dimmer_final, (dimmer_final-dimmer_initial)/nb_dots)
            else:
                liste_dimmer = [dimmer_initial]*nb_dots
            if color != self.light.color:
                liste_color = color.generate_array(self.light.color, nb_dots)
            else:
                #Logger.debug("on fait rien pour {}".format(self.light.name))
                self.light.disconnect() # on la deco si besoin
                barrier.wait()
                return

            err = self.light.connect()
            if err:
                Logger.debug("l'instruction sur "+self.light.name+" a planté")
                barrier.wait()
                self.light.deconnect(planté = True)
                return
            super().run(time_spent=(time()-delay))



            barrier.wait()
            for dim, value_color in zip(liste_dimmer, liste_color):
                if self.light.test():
                    raise SystemExit("kill inst")
                if not(err):
                    err1 = self.light.set_color(dim, value_color)
                    if err1:
                        break
                sleep(1/RESOLUTION)
                barrier.wait()
            if (not(err) and not(err1)):
                self.light.set_color(dimmer_final, color.value)
                self.light.disconnect()

        finally:
            Logger.info(" la led {} a mis {} s a s'allumer au lieu de {}".format(self.light.name, time()-delay, self.duration))
            self.light.unlock()
    
    def show(self):
        print("led = ",self.light.name, " | dimmer = ", self.dimmer, " | duration = ", self.duration, " | color = ",self.color)


