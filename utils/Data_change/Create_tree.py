from tree.Tree import Tree
from utils.Data_change.utils.Read import ouvrir, lire, trouver_dossier
from utils.Data_change.Create_env import get_env
from tree.Mode import Mode

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
    tree.liste_modes.show()

    # on va chercher les environnements
    # et on les remplits
    for nom in trouver_dossier(""):
        tree.liste_envi.add(get_env(nom))
    tree.show()
