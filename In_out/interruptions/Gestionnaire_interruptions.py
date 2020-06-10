from In_out.interruptions.Liste_interruptions import Liste_interruptions
from utils.Client import Client
import RPi.GPIO as GPIO

class Gestionnaire_interruptions:
    """
    liste toutes les différentes interruptions du rpi
    et leur lien avec l'arbre
    """

    GPIO.setmode(GPIO.BCM)

    client = Client() # on se connect à l'arbre
    listes_inters = [Liste_interruptions(12, 0x20, 1), Liste_interruptions(16,0x20,0)]

    #TODO bosse que sur le port extender, a faire pour les interruptions du rpi directement
    @classmethod
    def add_interruption(self, inter):
        self.listes_inters[inter.pin // 9].add(inter, inter.pin % 9)








