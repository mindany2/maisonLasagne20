from enum import Enum
from bluepy.btle import Peripheral

class TYPE_CONTROLER(Enum):
    NB_BROCHES_4 = 1
    NB_BROCHES_5 = 2


class Bluetooth:
    """
    Gère le bluetooth
    """
    def __init__(self, addr, type_led):
        self.addr = addr
        self.type_controler = type_led

    def connect(self):
        try:
            self.p = Peripheral(self.addr)
        except:
            return 1

        if self.type_controler == TYPE_CONTROLER.NB_BROCHES_4:
            self.serv = self.p.getServiceByUUID(0xfff0)
            self.char = self.serv.getCharacteristics(0xfff3)
        return 0

    def send(self, couleur_hex):
        if self.type_controler == TYPE_CONTROLER.NB_BROCHES_4:
            valeur = "0x7e070503"+couleur_hex[2::]+"10ef"
        print(valeur)
        valeur = int(valeur,16)
        valeur = valeur.to_bytes((valeur.bit_length()+7)//8,'big')
        self.char[0].write(valeur)

    def deconnect(self):
        self.p.disconnect()





