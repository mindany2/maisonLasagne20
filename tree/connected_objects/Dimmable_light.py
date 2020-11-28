from tree.connected_objects.Light import Light
from In_out.cartes.relais.Relais import Etat
from In_out.utils.ST_nucleo import ETAT_TRIAC
from enum import Enum
from time import sleep

class BULD(Enum):
    """
    Each dimmable light have is own range of dimmer
    """
    # type  = (maxi,mini)
    type_63 = (400,80)
    type_65 = (400,160)
    type_91 = (430,50)
    type_64 = (430,180)
    type_73 = (400,130)
    type_61 = (430,250)
    type_200 = (370,130)


class Dimmable_light(Light):
    """
    A dimmable light control by a triac
    """
    def __init__(self, name, triac, type_buld, relay = None):
        Light.__init__(self, name)
        self.triac = triac
        self.relay = relay
        self.type_buld = type_buld
        self.dimmer = 0
        # power off the light
        self.triac.set(10**9,ETAT_TRIAC.off)

    def connect(self):
        # setup dimmer if it is necessary
        if self.dimmer == 0:
            self.triac.set(self.convert(0))
        elif self.dimmer == 100:
            self.triac.set(self.convert(100))

    def disconnect(self):
        #disconnect if it is necessary
        if self.dimmer == 0:
            # setup dimmer
            self.triac.set(10**9, ETAT_TRIAC.off)
        elif self.dimmer == 100:
            # remove dimmer
            self.triac.set(10**9, ETAT_TRIAC.on)

    def set(self, dimmer):
        value = self.convert(dimmer)
        self.triac.set(value)
        self.dimmer = int(dimmer)

    def convert(self, dimmer):
        # convert dimmer value to triac value
        maxi, mini = self.type_buld.value
        value = int(mini + (maxi-mini)*(1-dimmer/100))
        return value
