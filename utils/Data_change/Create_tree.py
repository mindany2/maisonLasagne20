from tree.Tree import Tree
from utils.Data_change.utils.Read import ouvrir, lire, trouver_dossier
from utils.Data_change.Create_env import get_env
from utils.Data_change.Create_inputs import get_interrupteurs
from tree.Mode import Mode
from threading import Thread

import os

"""
Contient seulement les fonctions de lectures dans les fichiers
du programme (récupérations des infos)
"""

def get_tree():
    """
    genère un arbre avec tous les fichiers de data/Environnements
    """
    tree = Tree()

    #on va chercher les différents modes
    for mode in lire(ouvrir("modes.data")):
        tree.liste_modes.add(Mode(mode))

    # on va chercher les environnements
    # et on les remplits
    for nom in trouver_dossier(""):
        tree.liste_envi.add(get_env(nom))
    # on fait les inputs

    for env in tree.liste_envi:
        get_interrupteurs(env)
    
    process = Thread(target=env.liste_input.init)
    process.start()
    

    tree.show()
