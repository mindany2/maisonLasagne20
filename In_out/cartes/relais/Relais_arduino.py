from In_out.utils.Arduino import Arduino, MESSAGE_MASTER
from In_out.cartes.relais.Relais import Relais
from enum import Enum

class Relais_arduino(Relais):
    """
    Ceci est un relais
    """
    def __init__(self, message_on, message_off):
        Relais.__init__(self)
        self.message_on = message_on
        self.message_off = message_off

    def reload(self):
        if self.etat.value == 1:
            Arduino().send(self.message_on)
        else:
            Arduino().send(self.message_off)
