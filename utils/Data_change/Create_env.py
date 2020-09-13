from tree.Environnement import Environnement
from tree.Tree import Tree
from utils.Data_change.Create_lumière import get_lumiere
from utils.Data_change.Create_preset import get_preset
from utils.Data_change.utils.Read import ouvrir, lire, trouver_dossier
from tree.utils.Couleur import Couleur
from utils.Data_change.Create_styles import set_styles, set_env_style

def reload_env(env, liste_modes):
    env.reset_preset()
    get_infos(env, liste_modes)



def get_env(nom, liste_modes):
    """
    retourne un environnement complet
    """
    env = Environnement(nom) 
    
    #on recupére les lumières
    for lumière in lire(ouvrir(nom+"/lumieres.data")):
        env.add_lumiere(get_lumiere(lumière.split("|")))

    get_infos(env, liste_modes)

    return env

def get_infos(env, liste_modes):
    nom = env.nom
    # on recupére les presets
    for dossier in trouver_dossier("/"+nom+"/preset"):
        env.add_preset(get_preset(env,dossier))

    # on recupére les options
    # on commence par lire tout les informations utiles
    read_preset = False
    for ligne in lire(ouvrir(nom+"/option.data")):
        if ligne.count("Preset") != 0:
            # on lit la table des presets maintenant
            read_preset = True
        else : 
            args = ligne.split("=")
            arg1 = args[0]
            arg2 = args[1]
            if read_preset:
                # on lit des presets
                mode = Tree().get_mode(arg1)
                assert(mode != None)
                preset = env.get_preset(arg2)
                assert(preset != None)
                env.liste_presets_choisis.add(mode, preset)
            else:
                # on lit des paramètres
                if arg1 == "couleurs":
                    coul1, coul2 = arg2.split(",")
                    env.couleurs = (Couleur(coul1), Couleur(coul2))
    
                elif arg1 == "rang":
                    env.rang = int(arg2)

    # on met tous les styles pour avoir de joli boutons html
    for preset in env.liste_presets:
        set_styles(env, preset)
    set_env_style(env, liste_modes)


    # on met le même mode que le tree
    env.change_mode()











