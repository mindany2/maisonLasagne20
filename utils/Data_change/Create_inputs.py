from utils.Data_change.utils.Read import lire, ouvrir
from In_out.interruptions.inter.Interrupteur import Interrupteur
from In_out.interruptions.inter.Interruption import TYPE_INTER
from In_out.interruptions.inter.Interruption_arduino import Interruption_arduino
from In_out.interruptions.inter.Interruption_GPIO import Interruption_GPIO
from In_out.interruptions.inter.Interruption_date import Interruption_date
from In_out.interruptions.Gestionnaire_interruptions import Gestionnaire_interruptions

def get_interruptions():
    """
    On setup tout les inters
    """
    gestionnaire = Gestionnaire_interruptions()

    for ligne in lire(ouvrir("input.data", envs = False)):
        infos = ligne.split("|")
        nom = infos[1]
        type_inter = infos[2]
        pin = infos[3]
        if type_inter == "extender":
            type_inter = TYPE_INTER.extender
            inter = Interrupteur(nom, int(pin), gestionnaire.client, type_inter)
        elif type_inter == "gpio":
            type_inter = TYPE_INTER.rpi
            inter = Interruption_GPIO(nom, int(pin), gestionnaire.client, type_inter)
        elif type_inter == "cron":
            type_inter = TYPE_INTER.cron
            inter = Interruption_date(nom, pin, gestionnaire.client, type_inter)

        gestionnaire.add_interruption(inter)



