from time import time
from tree.Tree import Tree
from In_out.interruptions.inter.Interrupteur import Interrupteur
import RPi.GPIO as GPIO
from time import sleep
from utils.Logger import Logger

class Interruption_GPIO(Interrupteur):
    """
    Ceci est un interrupteur dans la maison
    """
    # mode pousoir par défaut

    def __init__(self, nom, pin, client, type_inter):
        Interrupteur.__init__(self, nom, pin, client, type_inter)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.press)
        self.valeur = GPIO.input(pin)
        Logger.debug("Valeur radar = {}".format(GPIO.input(pin)))
        if (GPIO.input(pin) == GPIO.LOW): # le radar est on des le debut
            sleep(1)
            super().press()

    def press(self, event):
        Logger.debug("Valeur radar = {}".format(GPIO.input(event)))
        if (self.valeur != GPIO.input(event)):
            self.valeur = GPIO.input(event)
            super().press(etat = not(self.valeur))
