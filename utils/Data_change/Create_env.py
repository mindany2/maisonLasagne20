from tree.Environnement import Environnement
from tree.Tree import Tree
from tree.Bouton import Bouton
from utils.Data_change.Create_lumière import get_lumiere
from utils.Data_change.Create_preset import get_preset
from utils.Data_change.utils.Read import ouvrir, lire, trouver_fichier

def get_env(nom):
    """
    retourne un environnement complet
    """
    env = Environnement(nom) 
    
    #on recupére les lumières
    for lumière in lire(ouvrir(nom+"/lumieres.data")):
        env.add_lumiere(get_lumiere(lumière.split("|")))

    # on recupére les presets
    for fichier in trouver_fichier("/"+nom+"/preset"):
        env.add_preset(get_preset(env,fichier))

    # on recupére les options
    # on commence par lire tout les informations utiles
    read_preset = False
    for ligne in lire(ouvrir(nom+"/option.data")):
        if ligne.count("Preset") != 0:
            # on lit la table des presets maintenant
            read_preset = True
        else : 
            args = ligne.split("=")
            print(args)
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
                if arg1 == "boutons_html":
                    if arg2 == "On" or arg2 == "on":
                        env.have_html_boutons = True
    
    # on a donc tous les paramètres de bases, maintenant on creer les boutons
    # donc un bouton par scénarios par preset selectionner

    for mode in env.liste_presets_choisis.keys():
        mode.show()
        print("ooooooooooooooooooooooo")
        preset = env.liste_presets_choisis.get(mode)
        for scenar in preset.liste_scénario:
            bt = Bouton(scenar.nom, mode, [scenar])
            env.add_boutons(bt)

    # maintenant que l'on a les boutons "normaux"
    # TODO les inputs


    print("fin env")
    return env 









