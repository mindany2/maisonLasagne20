from In_out.interruptions.inter.Interruption import TYPE_INTER
from utils.communication.Client import Client
from apscheduler.schedulers.blocking import BlockingScheduler
import RPi.GPIO as GPIO
from utils.Logger import Logger


class Gestionnaire_interruptions:
    """
    liste toutes les différentes interruptions du rpi
    et leur lien avec l'arbre
    """
    listes_inters_extender = []
    liste_inters_rpi = []
    listes_inters_date = []

    @classmethod
    def init(self):
        GPIO.setmode(GPIO.BCM)
        self.client = Client() # on se connect à l'arbre

    @classmethod
    def add_interruption(self, inter):
        if inter.type == TYPE_INTER.extender:
            self.listes_inters_extender[((inter.pin-1)//8)].add(inter, (inter.pin-1) % 8)
        elif inter.type == TYPE_INTER.rpi:
            self.liste_inters_rpi.append(inter)
        elif inter.type == TYPE_INTER.cron:
            self.listes_inters_date.append(inter)

    @classmethod
    def configure(self, interrupt, type_inter):
        if type_inter == TYPE_INTER.extender:
            self.listes_inters_extender.append(interrupt)
            print("ok")
        else:
            Logger.warn("pas la peine de renseigner les inters {} dans la configuration".format(type_inter))









