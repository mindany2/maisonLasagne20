from utils.Data_change.utils.Read import lire, ouvrir
from In_out.interruptions.utils.Interrupteur import Interrupteur
from In_out.interruptions.utils.Interruption_arduino import Interruption_arduino
from In_out.interruptions.Gestionnaire_interruptions import Gestionnaire_interruptions

def get_interruptions():
    """
    On setup tout les inters
    """
    gestionnaire = Gestionnaire_interruptions()

    for ligne in lire(ouvrir("input.data", envs = False)):
        infos = ligne.split("|")
        nom = infos[1]
        pin = int(infos[2])
        if nom.split("_")[0] == "inter":
            gestionnaire.add_interruption(Interrupteur(nom, pin, gestionnaire.client))
        elif nom == "arduino":
            gestionnaire.add_interruption(Interruption_arduino(nom, pin, gestionnaire.client))



