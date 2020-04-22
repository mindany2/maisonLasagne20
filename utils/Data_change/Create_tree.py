from tree.Tree import Tree
from utils.Data_change.utils.Read import ouvrir, lire, trouver_dossier
from utils.Data_change.Create_env import get_env
from utils.Data_change.Create_inputs import get_interrupteurs
from In_out.Liste_interrupteur import Liste_interrupteur
from web_app.boutons.Liste_boutons_html import Liste_boutons_html
from web_app.boutons.Bouton_html import Bouton_html
from tree.utils.boutons.Bouton_changement_mode import Bouton_changement_mode
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
        tree.add_mode(Mode(mode))


    # on va chercher les inters
    get_interrupteurs()

    

    # on va chercher les environnements
    # et on les remplits
    for nom in trouver_dossier(""):
        tree.liste_envi.add(get_env(nom))
    
    # on met le bouton changement de mode
    Liste_boutons_html().add_boutons_global(Bouton_changement_mode())
    
    # on lance les inters
    process = Thread(target=Liste_interrupteur().init)
    process.start()

    tree.show()
