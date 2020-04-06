from utils.Data_change.utils.Read import lire, ouvrir
from utils.In_out.Interrupteur import Interrupteur

def get_interrupteurs(env):
    """
    On setup tout les inters
    """
    liste = env.liste_input

    for ligne in lire(ouvrir(env.nom+"/input.data")):
        print(env.nom)
        print(ligne)
        infos = ligne.split("|")
        nom = infos[1]
        pin = int(infos[2])
        liste_boutons = infos[3].split(",")
        liste.add(Interrupteur(nom, pin, liste_boutons))



