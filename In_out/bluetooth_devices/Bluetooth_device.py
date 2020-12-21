from enum import Enum
from In_out.utils.Bluetooth import Bluetooth
from time import sleep
from tree.utils.Logger import Logger


def hex_to_byte(valeur):
   # convert hex to byte
   valeur = int(valeur,16)
   return valeur.to_bytes((valeur.bit_length()+7)//8,'big')

class Bluetooth_device:
    """
    Contains all the info to connect to a bluetooth device
    """
    def __init__(self, addr, uuid, char_id):
        self.addr = addr
        self.periph = None
        self.char = None
        self.uuid = uuid
        self.char_id = char_id

    def connect(self):
        compt = 0
        while self.periph == None:
            self.periph = Bluetooth().connect(self.addr)
            if self.periph: #!=None
                break
            else:
                compt += 1
                #Logger.warn("The device failed to connect : attempt n°" + str(compt))
                sleep(1)
            if compt == 10:
                Bluetooth.restart()
            if compt > 20:
                return False
        self.char = Bluetooth().get_char(self.periph, self.uuid, self.char_id)
        return True

    def send(self, valeur):
        err = Bluetooth().send(self.char, hex_to_byte(valeur))
        if err:
            # there are a connection error
            self.disconnect()
            sleep(1)
            # trying to reconnect
            self.connect()
            err = Bluetooth().send(self.char, hex_to_byte(valeur))
            if err:
                return 1
        return 0

    def disconnect(self, is_black = True):
        Bluetooth().disconnect(self.periph)
        if Bluetooth.nb_connection == 0 and is_black:
            Bluetooth.restart()
        self.periph = None
        self.char = None

    def __str__(self):
        return self.addr





