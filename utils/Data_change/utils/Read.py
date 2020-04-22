import os
PATH  ="/home/pi/maison/data/Environnements/"

def ouvrir(nom):
     return open(PATH+nom,"r")

def lire(fichier):
    liste = fichier.read().replace(" ","").replace("\t","").split("\n")
    for ligne in liste:
        if ligne != "" and ligne[0:2] != "\\" and ligne[0:2] != "//":
            yield ligne
    fichier.close()

def trouver_dossier(nom_sous_dossier):
    for nom in os.listdir(PATH[:-1]+nom_sous_dossier):
        if (os.path.isdir(PATH[:-1]+nom_sous_dossier+"/"+nom)):
            print(nom)
            yield nom

def trouver_fichier(nom_sous_dossier):
    for nom in os.listdir(PATH[:-1]+nom_sous_dossier):
        if (os.path.isfile(PATH[:-1]+nom_sous_dossier+"/"+nom)):
            yield nom



