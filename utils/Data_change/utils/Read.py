import os
PATH = "/home/pi/maison/data/"
PATH_ENV = PATH + "Environnements/"
def ouvrir(nom, envs = True):
     if envs:
         return open(PATH_ENV+nom,"r")
     return open(PATH+nom, "r")

def lire(fichier):
    liste = fichier.read().replace(" ","").replace("\t","").split("\n")
    for ligne in liste:
        if ligne != "" and ligne[0:2] != "\\" and ligne[0:2] != "//":
            yield ligne
    fichier.close()

def trouver_dossier(nom_sous_dossier):
    for nom in os.listdir(PATH_ENV[:-1]+nom_sous_dossier):
        if (os.path.isdir(PATH_ENV[:-1]+nom_sous_dossier+"/"+nom)):
            yield nom

def trouver_fichier(nom_sous_dossier):
    for nom in os.listdir(PATH_ENV[:-1]+nom_sous_dossier):
        if (os.path.isfile(PATH_ENV[:-1]+nom_sous_dossier+"/"+nom)):
            yield nom



    def repair(self):
        hs = list(self.liste_lumières)
        count = 0
        Logger.info("On reparre l'environnement " +self.nom)
        while hs != [] and count < 3:
            hs = []
            for lum in self.liste_lumières:
                Logger.info("On repare la lumières " + lum.nom)
                if lum.repair():
                    hs.append(lum)
            # on reset le wifi
            if hs != []:
                count += 1
                check_for_reset()
        if hs != []:
            Logger.error("--------------  Environnement : {} --------------".format(self.nom))
            for lum in hs:
                Logger.error(" ---------- LED {} est totalement HS ----------".format(lum.nom))
            
