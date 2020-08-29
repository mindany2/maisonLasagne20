from utils.Data_change.utils.Read import ouvrir, lire
from tree.Preset import Preset
from tree.eclairage.Led import Led
from tree.eclairage.Lampe import Lampe
from tree.eclairage.Enceintes import Enceintes
from tree.eclairage.Trappe import Trappe
from tree.scenario.Instruction_led import Instruction_led
from tree.scenario.Instruction_projecteur import Instruction_projecteur
from tree.scenario.Instruction_lampe import Instruction_lampe
from tree.scenario.Instruction_bouton import Instruction_bouton
from tree.scenario.Instruction_trappe import Instruction_trappe
from tree.scenario.Instruction_enceinte import Instruction_enceinte
from tree.eclairage.Projecteur import Projecteur
from tree.scenario.Scenario import Scenario,MARQUEUR
from tree.boutons.Bouton_simple import Bouton_simple
from tree.boutons.Bouton_principal import Bouton_principal
from tree.boutons.Bouton_poussoir import Bouton_poussoir
from tree.boutons.Bouton_deco import Bouton_deco
from tree.boutons.Bouton_etat import Bouton_etat
from tree.boutons.Bouton_choix import Bouton_choix
from tree.boutons.html.Bouton_simple_html import Bouton_simple_html
from tree.boutons.html.Bouton_unique_html import Bouton_unique_html


def get_preset(env, nom):
    """
    On recupére la preset
    """
    preset = Preset(nom)
    # on lit les scenarios et on les stockent
    scenar = None
    for ligne in lire(ouvrir(env.nom+"/preset/"+nom+"/scenarios.data")):
        if ligne.count("|") == 0:
            # on est sur la premiere ligne
            if ligne.count(":") == 1:
                (nom_scenar, marqueur) = ligne.split(":")
                #on a un marqueur on/off
                if marqueur == "deco" or marqueur == "déco":
                    marqueur = MARQUEUR.DECO
                elif marqueur == "off":
                    marqueur = MARQUEUR.OFF
                else:
                    marqueur = MARQUEUR.ON
            else:
                nom_scenar = ligne
                # on suppose que c'est on
                if nom_scenar != "eteindre":
                    marqueur = MARQUEUR.ON
                else:
                    marqueur = MARQUEUR.OFF
            # on créer donc un nv scenar
            scenar = Scenario(nom_scenar, marqueur)
            preset.add_scenar(scenar)
        elif scenar != None:
            inst = get_inst(env,ligne.split("|"))
            if inst != None:
                scenar.add_inst(inst)
            else:
                raise(IOError("Erreur de lecture : env = {}, preset = {}, scenar = {}".format(env.nom, preset.nom, scenar.nom)))
                

    # maintenant on lie la liste des boutons html et inters utilisé avec le bon scenario

    for ligne in lire(ouvrir(env.nom+"/preset/"+nom+"/boutons.data")):
        (vide, nom_bt, type_bt, nom_scenar, mode) = ligne.split("|") 
        if type_bt == "html":
            if mode == "simple":
               scenar = preset.get_scenar(nom_scenar)
               check(env, preset,scenar, nom_scenar)
               bt = Bouton_simple_html(nom_bt, scenar)
            if mode == "unique":
               scenar_on = preset.get_scenar(nom_scenar.split(",")[0])
               scenar_off = preset.get_scenar(nom_scenar.split(",")[1])
               check(env, preset, scenar_on, nom_scenar)
               check(env, preset, scenar_off, nom_scenar)
               bt = Bouton_unique_html(nom_bt, scenar_on, scenar_off)
            preset.add_boutons_html(bt)
        elif type_bt == "inter":
            if mode == "principal":
               scenar_on = preset.get_scenar(nom_scenar.split(",")[0])
               scenar_off = preset.get_scenar(nom_scenar.split(",")[1])
               check(env, preset, scenar_on, nom_scenar)
               check(env, preset, scenar_off, nom_scenar)
               bt = Bouton_principal(nom_bt, env, scenar_on, scenar_off)

            elif mode == "etat" or mode == "radar":
               scenar_on = preset.get_scenar(nom_scenar.split(",")[0])
               scenar_off = preset.get_scenar(nom_scenar.split(",")[1])
               check(env, preset, scenar_on, nom_scenar)
               check(env, preset, scenar_off, nom_scenar)
               bt = Bouton_etat(nom_bt, env, scenar_on, scenar_off)

            elif mode == "poussoir":
               scenar = preset.get_scenar(nom_scenar)
               check(env, preset,scenar, nom_scenar)
               bt = Bouton_poussoir(nom_bt, env, scenar)

            elif mode == "deco":
               scenar = preset.get_scenar(nom_scenar)
               check(env, preset,scenar, nom_scenar)
               bt = Bouton_deco(nom_bt, env, scenar)

            elif mode =="choix":
                liste_nom = nom_scenar.split(",")
                liste_scenar = [check(env, preset, preset.get_scenar(nom), nom) for nom in liste_nom]
                bt = Bouton_choix(nom_bt, env, liste_scenar)

            elif mode == "simple":
               scenar = preset.get_scenar(nom_scenar)
               check(env, preset,scenar, nom_scenar)
               bt = Bouton_simple(nom_bt, scenar)
            else:
                raise(Exception("Le type de bouton \"{}\" dans la preset {} de {} n'existe pas".format(mode,preset.nom,env.nom)))
            preset.add_lien_inter(nom_bt, bt)

    return preset

def check(env, preset, scenar, nom_scenar):
    if scenar == None:
        raise(Exception(("Le scenario {} dans l'environnement {} preset {} n'existe pas".format(nom_scenar, env.nom, preset.nom))))
    return scenar

def get_inst(env, infos):
    """
    Créer une instruction
    """
    nom_lampe = infos[1]
    temps_init = int(infos[4])
    try:
        synchro = infos[6] == "oui"
    except:
        synchro = False
    if (nom_lampe.count(".") != 0):
        # on a une instruction bouton
        nom_env, nom_preset, nom_scenar = nom_lampe.split(".")
        etat = int(infos[2])
        type_bt = infos[3]
        temps_init = int(infos[4])
        if (type_bt != "deco" and type_bt != "unique"):
            raise(Exception("Type bouton non supporter {} : {}".format(env.nom, type_bt)))

        return Instruction_bouton(nom_env, nom_preset, nom_scenar, etat, type_bt, temps_init, synchro)




    dimmeur = infos[2]
    duree = int(infos[3])
    couleur = infos[5]
    
    lumière = env.get_lumiere(nom_lampe)
    if isinstance(lumière, Projecteur):
        return Instruction_projecteur(lumière, int(dimmeur), duree, temps_init, synchro)
    elif isinstance(lumière, Led):
        return Instruction_led(lumière, int(dimmeur), duree, temps_init, synchro, couleur)
    elif isinstance(lumière, Lampe):
        return Instruction_lampe(lumière, int(dimmeur), temps_init, synchro)
    elif isinstance(lumière, Trappe):
        action = dimmeur
        return Instruction_trappe(action,duree, temps_init, synchro)
    elif isinstance(lumière, Enceintes):
        return Instruction_enceinte(lumière, int(dimmeur), duree, temps_init, synchro) 

    return None

