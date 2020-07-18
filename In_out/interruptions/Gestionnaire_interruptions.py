from In_out.interruptions.Liste_interruptions import Liste_interruptions
from In_out.interruptions.inter.Interruption import TYPE_INTER
from utils.Client import Client
import RPi.GPIO as GPIO


class Gestionnaire_interruptions:
    """
    liste toutes les différentes interruptions du rpi
    et leur lien avec l'arbre
    """
    listes_inters_extender = []

    @classmethod
    def init(self):
        GPIO.setmode(GPIO.BCM)

        self.client = Client() # on se connect à l'arbre

    #TODO bosse que sur le port extender, a faire pour les interruptions du rpi directement
    @classmethod
    def add_interruption(self, inter):
        if inter.type == TYPE_INTER.extender:
            self.listes_inters_extender[(inter.pin//9)].add(inter, (inter.pin-1) % 8)

    @classmethod
    def configure(self, interrupt, type_inter):
        if type_inter == TYPE_INTER.extender:
            self.listes_inters_extender.append(interrupt)








