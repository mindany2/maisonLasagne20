from In_out.interruptions.inter.Interruption import TYPE_INTER
from utils.communication.Client import Client
import RPi.GPIO as GPIO
from utils.Logger import Logger


class Gestionnaire_interruptions:
    """
    liste toutes les différentes interruptions du rpi
    et leur lien avec l'arbre
    """
    listes_inters_extender = []
    liste_inters_rpi = []

    @classmethod
    def init(self):
        GPIO.setmode(GPIO.BCM)

        self.client = Client() # on se connect à l'arbre

    @classmethod
    def add_interruption(self, inter):
        if inter.type == TYPE_INTER.extender:
            self.listes_inters_extender[(inter.pin//9)].add(inter, (inter.pin-1) % 8)
        elif inter.type == TYPE_INTER.rpi:
            self.liste_inters_rpi.append(inter)

    @classmethod
    def configure(self, interrupt, type_inter):
        if type_inter == TYPE_INTER.extender:
            self.listes_inters_extender.append(interrupt)
        elif type_inter == TYPE_INTER.rpi:
            Logger.warn("pas la peine de renseigner les inters rpi dans la configuration")









