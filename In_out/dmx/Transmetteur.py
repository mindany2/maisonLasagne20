from time import time, sleep
from In_out.cartes.relais.Relais import Etat
from threading import Thread

TIME_OUT = 3
CONNECTION_TIME = 2

class Transmetteur:
    """
    Controle le relais d'un transmetter
    sans fil dmx
    """
    def __init__(self, relais, addr_min, addr_max):
        self.relais = relais
        self.addr_min = addr_min
        self.addr_max = addr_max

        self.temps = time()

    def etat(self):
        return self.relais.etat == Etat.ON

    def test(self, addr):
        if self.addr_min <= addr and addr <= self.addr_max:
            self.temps = time()
            if not(self.etat()):
                self.relais.set(Etat.ON)
                sleep(CONNECTION_TIME) # temps de connection
                Thread(target = self.check_for_deconnection).start()

    def check_for_deconnection(self):
        while time()-self.temps < TIME_OUT:
            sleep(1)
        self.relais.set(Etat.OFF)
        
