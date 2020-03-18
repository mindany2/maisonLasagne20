from tree.Liste_environnements import Liste_environnements
from tree.Environnement import Environnement
from tree.Liste_boutons import Liste_boutons
from tree.Liste_boutons_radios import Liste_boutons_radios
from tree.Bouton import Bouton
from tree.Tree import Tree
from tree.scenario.Instruction import Instruction
from tree.eclairage.Liste_lumieres import Liste_lumieres
from tree.eclairage.Led import Led
from tree.eclairage.Projecteur import Projecteur
from tree.Bouton_html import Bouton_html
from tree.scenario.Instruction_sleep import Instruction_sleep
from tree.scenario.Instruction_led import Instruction_led
from tree.scenario.Instruction_projecteur import Instruction_projecteur

PATH  ="/home/pi/maison/data/Environnements/"
MODE_RP = 1
from utils.controle.Controle import Controle
from utils.controle.Bluetooth import TYPE_CONTROLER
try:
    from utils.controle.Controle import Controle
    from utils.controle.Bluetooth import TYPE_CONTROLER
except:
    PATH  ="/home/lasagne/maison/data/Environnements/"
    MODE_RP = 0

import os

"""
Contient seulement les fonctions de lectures dans les fichiers
du programme (récupérations des infos)
"""

def get_tree():
    """
    genère un arbre avec tous les fichiers
    """
    tree = Tree().liste_envi

    # on va chercher les environnements
    for i,env in enumerate(os.listdir(PATH[:-1])):
        if (os.path.isdir(PATH+env)):
            tree.add(get_env(env,i))
    tree.show()

def get_env(nom, index):
    """
    retourne un environnement complet
    """
    env = Environnement(nom, index) 

    fichier_map = open(PATH+nom+"/map.data","r")
    env.liste_lumières = get_map(fichier_map)
    fichier_map.close()
    
    fichier_bouton = open(PATH+nom+"/boutons.data","r")
    env.liste_boutons = get_boutons(fichier_bouton, env)
    fichier_bouton.close()


    return env 

def get_map(fichier):
    """
    Créer toutes les lumières de l'env
    """
    liste = Liste_lumieres()
    #on saute les 4 premières lignes
    for _ in range(0,4):
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
        triac = 0
        if MODE_RP:
            triac = Controle().get_triac(int(ligne[3][2]), int(ligne[3][0]))
        return Projecteur(ligne[0], triac)

    elif ligne[1][0:3] == "led":
        relais = 0
        type_led = 42
        if MODE_RP:
            relais = Controle().get_relais(int(ligne[2][2]), int(ligne[2][0]))
            if ligne[1][4] == "4":
                type_led = TYPE_CONTROLER.NB_BROCHES_4
            else:
                type_led = TYPE_CONTROLER.NB_BROCHES_5

        return Led(ligne[0], relais, ligne[4], type_led, ligne[5])
        

def get_boutons(fichier, env):
    """
    Créer tous les boutons avec leurs instructions
    """
    liste = Liste_boutons_radios()
    #on saute les 3 premières lignes
    for _ in range(0,3):
        fichier.readline()
    #on store la d'index de la page
    index = fichier.readline().replace("\n","")
    
    #on parcours tous les boutons
    #on saute une ligne
    ligne = fichier.readline()
    compteur = 0
    while ligne:
        bouton = get_bouton(fichier, compteur, env)
        liste.add(bouton)
        #on saute une ligne a chaque bouton (numero)
        ligne = fichier.readline()
        compteur += 1

    return liste

def get_bouton(fichier, numero, env):
    """
    Créer un bouton
    """
    ligne = fichier.readline().replace(" ","").replace("\t","").replace("\n","").split(":")
    nom = ligne[0]
    bouton = Bouton_html(nom, env.nom, (env.position,numero))
    # on met les paramètres
    params = ligne[1].replace("(","").replace(")","").split(",")
    for par in params:
        pass
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
        return Instruction_projecteur(env.liste_lumières.get(lum), dimmeur, duree, attente)
    elif (type_inst == "led"):
        return Instruction_led(env.liste_lumières.get(lum), dimmeur, duree, ligne[6], attente)
    raise(IOError)
        










