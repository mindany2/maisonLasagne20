import os
from enum import Enum

class DATA(Enum):
    Bouton = "bouton.data"
    Map = "map.data"

def set_last_color_led(led):
   couleur = led.couleur 
   nom = led.nom
   #fichier, ligne = locate_element(nom, DATA.Map)
   #print(ligne)


def locate_element(nom, data):  
    PATH  ="/home/lasagne/maison/data/Environnements"
    for dossier in os.listdir(PATH):
        if os.path.isdir(PATH + "/"+dossier):
            fichier = open(PATH+"/"+dossier + "/"+data.value,"r+")
            for ligne in fichier:
                if ligne.count(nom) != 0:
                    return fichier, ligne

    raise("Erreur : "+nom+" non trouvé dans le fichier "+data.value)

