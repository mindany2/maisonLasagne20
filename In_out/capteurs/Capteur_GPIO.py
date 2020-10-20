from In_out.capteurs.Capteur import Capteur
import RPi.GPIO as GPIO
from time import sleep,time

class Capteur_GPIO(Capteur):
    
    def __init__(self, nom, pin):
        Capteur.__init__(self, nom)
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.capture()

    def capture(self):
        self.etat = GPIO.input(self.pin)
        return self.etat

    def wait_until_change(self, time_out):
        etat = self.etat
        temps = time()
        while (etat == self.etat and ((time()-temps) < time_out)):
            self.capture()
            sleep(0.2)

