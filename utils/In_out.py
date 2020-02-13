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

import os

"""
Contient seulement les fonctions de lectures dans les fichiers
du programme (récupérations des infos)
"""
PATH  ="/home/pi/maison/data/Environnements/"

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
    env.liste_boutons = get_boutons(app, fichier_bouton, tree.liste_info)
    fichier_bouton.close()

    return env 

def get_map(fichier):
    """
    Créer toutes les lumières de l'env
    """
    liste = Liste_lumieres()
    #on saute les 4 premières lignes
    for i in range(0,4):
        fichier.readline()
    print("---- Lumières ----")
    ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split("|")
    while ligne != ['']:
        print(ligne)
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
        

def get_boutons(app, fichier, liste_info):
    """
    Créer tous les boutons avec leurs instructions
    """
    liste = Liste_boutons(liste_info)
    #on saute les 3 premières lignes
    for _ in range(0,3):
        fichier.readline()
    #on store la d'index de la page
    index = fichier.readline().replace("\n","")
    
    #on parcours tous les boutons
    continu = True
    while continu:
        bouton, continu = get_bouton(app, fichier, liste_info, index)
        liste.add(bouton)

    return liste

def get_bouton(app, fichier, liste_info, index):
    """
    Créer un bouton
    """
    #on saute une ligne
    fichier.readline()
    ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split(":")
    print("ici : ",ligne)
    nom = ligne[0]
    bouton = Bouton_html(nom, index, app, liste_info)
    # on met les paramètres
    params = ligne[1].replace("(","").replace(")","").split(",")
    print(params)
    for par in params:
        oui = par.split("/")[0]
        non = par.split("/")[1]
        bouton.add_param(oui, non)

    #TODO faire recupération instructions

    return bouton, False
        












