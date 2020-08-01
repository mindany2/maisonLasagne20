from In_out.utils.Arduino import Arduino, MESSAGE_MASTER
from In_out.cartes.relais.Relais import Relais
from enum import Enum
import RPi.GPIO as GPIO

class Relais_GPIO(Relais):
    """
    Ceci est un relais
    """
    def __init__(self, pin):
        Relais.__init__(self)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        self.pin = pin


    def reload(self):
        GPIO.output(self.pin,(self.etat.value * GPIO.LOW) + (not(self.etat.value) *  GPIO.HIGH))
