from In_out.utils.DAX66 import DAX66
from In_out.son.Zone import Zone
from In_out.cartes.relais.Relais import Etat
from utils.Logger import Logger
from time import sleep

class Ampli_6_zones:
    """
    Gere l'ampli DAX66
    """

    @classmethod
    def init(self, addr, relais):
        self.bus = DAX66(addr)
        self.relais = relais
        
        self.zones = [Zone(i, self.bus) for i in range(1,7)]

    @classmethod
    def etat(self):
        return self.relais.etat == Etat.ON

    @classmethod
    def get_zone(self, i):
        try:
            return self.zones[i-1]
        except:
            Logger.error("L'ampli n'est pas initialiser")
            return None
            

    @classmethod
    def allumer(self):
        if not(self.etat()):
            self.relais.set(Etat.ON)
            sleep(5)

    @classmethod
    def eteindre(self):
        if self.etat():
            # on attend que toutes les zones soient eteintes
            for zone in self.zones:
                if zone.power:
                    return
            self.relais.set(Etat.OFF)
