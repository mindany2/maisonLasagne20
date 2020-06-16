from In_out.utils.I2C import I2C
from enum import Enum
from time import sleep
from threading import Lock
import RPi.GPIO as GPIO
from tree.Tree import Tree

class ETAT_TRIAC(Enum):
    """
    Donne l'ordre au triac de rester allumer
    si on met une valeur impossible à atteindre
    """
    dimmer = 0
    on = 1
    off = 2


class ST_nucleo:
    """
    Carte pour les triacs
    """

    i2c = I2C()
    ip = 0x10

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.OUT, initial = GPIO.HIGH) # reset_st_carte

    @classmethod
    def set(self, carte, triac, valeur, etat):
        v1 = valeur // 255
        v2 = valeur  % 255
        err = self.i2c.write_data(self.ip, [carte, triac, v1, v2, etat.value])
        if err:
            self.reset()
        sleep(0.004)

    @classmethod
    def reset(self):
        # on reset la carte
        print("ooooooonnnnnnnnnnn rrrrrrrrrrreeeeeeeeeeeeeesssssssssssssseeeeeeeeeeeeettttttttttt la carte")
        GPIO.output(13, GPIO.LOW)
        sleep(0.01)
        GPIO.output(13, GPIO.HIGH)
        proc = Thread(target=Tree().refresh_all_projo)
        proc.start()


