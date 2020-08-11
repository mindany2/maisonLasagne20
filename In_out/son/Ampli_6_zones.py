from In_out.utils.DAX66 import DAX66
from In_out.son.Zone import Zone
from In_out.cartes.relais.Relais import ETAT
from time import sleep

class Ampli_6_zones:
    """
    Gere l'ampli DAX66
    """

    def __init__(self, addr, relais):
        self.bus = DAX66(addr)
        self.relais = relais
        
        self.zones = [Zone(i, self.bus) for i in range(1,10)]

    def etat(self):
        return self.relais.etat.value

    def allumer(self):
        if not(self.etat):
            self.relais.set(ETAT.ON)
            sleep(5)

            for zone in self.zones:
                zone.reload()
