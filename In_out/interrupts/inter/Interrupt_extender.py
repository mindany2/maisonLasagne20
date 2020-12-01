from time import time
from In_out.interrupts.inter.Interrupt import Interrupt
from In_out.network.communication.interrupt.Press_inter import Press_inter

class Interrupt_extender(Interrupt):
    """
    This is a button with a pin from the extender
    """

    def __init__(self, name, pin, client):
        Interrupt.__init__(self, name, client)
        self.pin = pin
        self.tps = time()

    def press(self, state = 1):
        if ((time() - self.tps) > 1):     # allow to take only one push
            self.client.send(Press_inter(self.name, state))
            self.tps = time() 

