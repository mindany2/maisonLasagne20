from web_app.site_maison import Site_maison
from tree.Liste_environnements import Liste_environnements
from tree.Environnement import Environnement
from tree.Liste_boutons import Liste_boutons
from tree.Bouton import Bouton
from scenario.Instruction import Instruction
from eclairage.Liste_lumieres import Liste_lumieres
from eclairage.Led import Led
from eclairage.Projecteur import Projecteur
from web_app.Bouton_html import Bouton_html
from scenario.Instruction_sleep import Instruction_sleep
from scenario.Instruction_led import Instruction_led
from scenario.Instruction_projecteur import Instruction_projecteur

import os

"""
Contient seulement les fonctions de lectures dans les fichiers
du programme (récupérations des infos)
"""
PATH  ="./data/Environnements/"

def get_tree(app):
    """
    genère un arbre avec tous les fichiers
    """
    tree = Liste_environnements()

    # on va chercher les environnements
    for env in os.listdir(PATH[:-1]):
        if (os.path.isdir(PATH+env)):
            print(env)
            tree.add(get_env(app, tree, env))

    return tree

def get_env(app, tree, nom):
    """
    retourne un environnement complet
    """
    env = Environnement(nom, tree.liste_info) 

    fichier_map = open(PATH+nom+"/map.data","r")
    env.liste_lumières = get_map(fichier_map)
    fichier_map.close()
    
    fichier_bouton = open(PATH+nom+"/boutons.data","r")
    env.liste_boutons = get_boutons(app, fichier_bouton, tree.liste_info, env)
    fichier_bouton.close()

    env.show()

    return env 

def get_map(fichier):
    """
    Créer toutes les lumières de l'env
    """
    liste = Liste_lumieres()
    #on saute les 4 premières lignes
    for i in range(0,4):
        fichier.readline()
    ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split("|")
    while ligne != ['']:
        liste.add(get_lumiere(ligne))
        ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split("|")
    return liste

def get_lumiere(ligne):
    """
    Créer la lumière correspondante avec les bonnes infos
    """
    if ligne[1] == "projo":
        return Projecteur(ligne[0], int(ligne[2]))

    elif ligne[1] == "led":
        return Led(ligne[0], int(ligne[2]), ligne[3], ligne[4])
        

def get_boutons(app, fichier, liste_info, env):
    """
    Créer tous les boutons avec leurs instructions
    """
    liste = Liste_boutons(liste_info)
    #on saute les 3 premières lignes
    for _ in range(0,3):
        fichier.readline()
    #on store la d'index de la page
    index = fichier.readline()
    
    #on parcours tous les boutons
    #on saute une ligne
    ligne = fichier.readline()
    while ligne:
        bouton = get_bouton(app, fichier, liste_info, index, env)
        liste.add(bouton)
        #on saute une ligne a chaque bouton (numero)
        ligne = fichier.readline()

    return liste

def get_bouton(app, fichier, liste_info, index, env):
    """
    Créer un bouton
    """
    ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split(":")
    nom = ligne[0]
    bouton = Bouton_html(nom, index, app, liste_info)
    # on met les paramètres
    params = ligne[1].replace("(","").replace(")","").split(",")
    for par in params:
        oui = par.split("/")[0]
        non = par.split("/")[1]
        bouton.add_param(oui, non)
    #on saute 2 lignes
    fichier.readline()
    fichier.readline()

    # on recupére les instructions
    ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split("|")
    while ligne != ['']:
        inst = get_inst(ligne, env)
        bouton.add_inst(inst)
        ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split("|")
        
    return bouton

def get_inst(ligne, env):
    """
    Créer une instruction
    """
    type_inst = ligne[1]
    duree = int(ligne[4])
    if (type_inst == "sleep"):
        return Instruction_sleep(duree)
    # on a une lumière
    lum = ligne[2]
    dimmeur = int(ligne[3])
    attente = (ligne[5] == "oui")
    if (type_inst == "projo"):
        return Instruction_projecteur(env.liste_lumières.get(lum), dimmeur, duree)
    elif (type_inst == "led"):
        return Instruction_led(env.liste_lumières.get(lum), dimmeur, duree, ligne[6])
    print("Erreur")
    return 0
        












