from eclairage.Lumiere import Lumiere
import RPi.GPIO as GPIO

class Projecteur(Lumiere):
    """
    Un projecteur simple sur un dyrak
    """
    def __init__(this, nom, pin_addr):
        Lumiere.__init__(nom, pin_addr)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_addr, GPIO.OUT, initial = GPIO.HIGH)


    def set(this, dimmeur):
        this.dimmeur = dimmeur
        # on utilise ici la sortie
        #du raspberry
        liste = [GPIO.LOW, GPIO.HIGH]
        GPIO.outpout(3, liste[dimmeur == 0])

        
