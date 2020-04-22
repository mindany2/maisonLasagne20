from utils.Data_change.utils.Read import lire, ouvrir
from In_out.Interrupteur import Interrupteur
from In_out.Liste_interrupteur import Liste_interrupteur

def get_interrupteurs():
    """
    On setup tout les inters
    """
    liste = Liste_interrupteur()

    for ligne in lire(ouvrir("input.data")):
        infos = ligne.split("|")
        nom = infos[1]
        pin = int(infos[2])
        liste.add(Interrupteur(nom, pin))



