from time import time
from In_out.interrupts.inter.Interrupt import Interrupt
from In_out.network.messages.interrupt.Press_inter import Press_inter

class Interrupt_extender(Interrupt):
    """
    This is a button with a pin from the extender
    """

    def __init__(self, name, name_env, pin, client):
        Interrupt.__init__(self, name, name_env, client)
        self.pin = pin
        self.tps = time()

    def press(self):
        if ((time() - self.tps) > 1):     # allow to take only one push
            super().press()
            self.tps = time() 

    def __str__(self):
        return super().__str__() + " : {}".format(self.pin)

