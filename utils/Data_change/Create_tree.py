from tree.Tree import Tree
from utils.Data_change.utils.Read import ouvrir, lire, trouver_dossier
from utils.Data_change.Create_env import get_env,reload_env
from utils.Data_change.Create_inputs import get_interrupteurs
from In_out.Liste_interrupteur import Liste_interrupteur
from tree.boutons.Bouton_changement_mode import Bouton_changement_mode
from tree.Mode import Mode
from threading import Thread

import os

"""
Contient seulement les fonctions de lectures dans les fichiers
du programme (récupérations des infos)
"""
def reload_tree():
    for env in Tree().liste_envi:
        reload_env(env)
        


def get_tree():
    """
    genère un arbre avec tous les fichiers de data/Environnements
    """
    tree = Tree()

    #on va chercher les différents modes
    for mode in lire(ouvrir("modes.data")):
        nom_mode = mode.split(":")[0]
        css_file = mode.split(":")[1]
        tree.add_mode(Mode(nom_mode, css_file))


    # on va chercher les inters
    get_interrupteurs()

    
    # on va chercher les environnements
    # et on les remplits
    for nom in trouver_dossier(""):
        tree.liste_envi.add(get_env(nom))
    
    # on met le bouton changement de mode
    
    # on lance les inters
    process = Thread(target=Liste_interrupteur().init)
    process.start()

    #tree.show()
