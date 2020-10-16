from In_out.utils.DAX66 import DAX66
from In_out.son.Zone import Zone
from In_out.cartes.relais.Relais import Etat
from utils.spotify.Spotify import Spotify
from utils.Logger import Logger
from time import sleep
from threading import Lock

class Ampli_6_zones:
    """
    Gere l'ampli DAX66
    """

    @classmethod
    def init(self, addr, relais):
        self.bus = DAX66(addr)
        self.relais = relais
        self.mutex = Lock()
        
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
        self.mutex.acquire()
        print("etat = " + str(self.etat()))
        if not(self.etat()):
            Logger.debug("on allume l'ampli")
            self.relais.set(Etat.ON)
            sleep(1)
            conn = self.bus.connect()
            if not(conn):
                self.relais.set(Etat.OFF)

            for zone in self.zones:
                zone.get_infos()
            print("etat = " + str(self.etat()))
            print("on start spotify")
            Spotify().start()
        self.mutex.release()

    @classmethod
    def eteindre(self):
        self.mutex.acquire()
        if self.etat():
            # on check si toutes les zones sont eteintes
            test = True
            for zone in self.zones:
                if zone.power:
                    test = False
            if test:
                self.bus.deconnect()
                self.relais.set(Etat.OFF)
                Logger.debug("on eteint l'ampli")
                Spotify.kill()
        self.mutex.release()
