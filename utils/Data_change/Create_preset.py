from utils.Data_change.utils.Read import ouvrir, lire
from tree.Preset import Preset
from tree.eclairage.Led import Led
from tree.eclairage.Lampe import Lampe
from tree.eclairage.Enceintes import Enceintes
from tree.eclairage.dmx.Lyre import Lyre, COULEUR, GOBO
from tree.eclairage.Trappe import Trappe
from tree.utils.Variable import Variable

from tree.scenario.Instruction_led import Instruction_led
from tree.scenario.Instruction_projecteur import Instruction_projecteur
from tree.scenario.Instruction_lampe import Instruction_lampe
from tree.scenario.Instruction_variable import Instruction_variable, TYPE_INST
from tree.scenario.Instruction_bouton import Instruction_bouton, TYPE_BOUTON
from tree.scenario.Instruction_trappe import Instruction_trappe, INST_TRAPPE
from tree.scenario.Instruction_enceinte import Instruction_enceinte
from tree.scenario.Instruction_spotify import Instruction_spotify, TYPE_INST_SPOTIFY
from tree.scenario.dmx.Instruction_position import Instruction_position
from tree.scenario.dmx.Instruction_gobo import Instruction_gobo
from tree.scenario.dmx.Instruction_dimmeur import Instruction_dimmeur
from tree.scenario.dmx.Instruction_couleur import Instruction_couleur
from tree.scenario.dmx.Instruction_strombo import Instruction_strombo
from tree.scenario.dmx.Instruction_program import Instruction_program
from tree.scenario.dmx.Instruction_vitesse import Instruction_vitesse
from tree.eclairage.Projecteur import Projecteur
from tree.scenario.Scenario import Scenario,MARQUEUR
from tree.eclairage.dmx.Boule import Boule
from tree.eclairage.dmx.Laser import Laser
from tree.eclairage.dmx.Strombo import Strombo
from tree.eclairage.dmx.Decoupe import Decoupe

from tree.boutons.Bouton_simple import Bouton_simple
from tree.boutons.Bouton_principal import Bouton_principal
from tree.boutons.Bouton_poussoir import Bouton_poussoir
from tree.boutons.Bouton_unique import Bouton_unique
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
                if nom_scenar.count("eteindre") == 0:
                    marqueur = MARQUEUR.ON
                else:
                    marqueur = MARQUEUR.OFF
            if ligne.count("*") == 0:
                boucle = False
            else:
                boucle = True
            # on créer donc un nv scenar
            scenar = Scenario(nom_scenar.replace("*",""), marqueur, env.calculateur, boucle)
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
               bt = Bouton_simple_html(nom_bt, env, scenar)
            if mode == "unique":
               scenar_on = preset.get_scenar(nom_scenar.split(",")[0])
               scenar_off = preset.get_scenar(nom_scenar.split(",")[1])
               check(env, preset, scenar_on, nom_scenar)
               check(env, preset, scenar_off, nom_scenar)
               bt = Bouton_unique_html(nom_bt, env, scenar_on, scenar_off)
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

            elif mode == "unique":
               liste_nom = nom_scenar.split(",")
               liste_scenar = [check(env, preset, preset.get_scenar(nom), nom) for nom in liste_nom]
               bt = Bouton_unique(nom_bt, env, liste_scenar[0], liste_scenar[1])
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
    dimmeur = infos[2]
    duree = infos[3]
    try:
        synchro = infos[6] == "oui"
    except:
        synchro = False
    if (nom_lampe.count(".") != 0):
        # on a une instruction bouton
        nom_env, nom_preset, nom_scenar = nom_lampe.split(".")
        type_bt = infos[2]
        temps_init = infos[3]
        try:
            condition = infos[4]
            if condition == "":
                condition = True
        except:
            condition = True
        if type_bt == "déco" or type_bt == "deco":
            type_bt = TYPE_BOUTON.deco
        elif type_bt == "scenar" or type_bt == "scénar":
            type_bt = TYPE_BOUTON.scenar
        elif type_bt == "poussoir":
            type_bt = TYPE_BOUTON.poussoir

        return Instruction_bouton(nom_env, nom_preset, nom_scenar, type_bt, temps_init, synchro, condition)

    elif nom_lampe == "spotify":
        return Instruction_spotify(TYPE_INST_SPOTIFY[dimmeur], temps_init, synchro, duree)

    temps_init = infos[4]
    couleur = infos[5]

    
    lumière = env.get_lumiere(nom_lampe)
    if isinstance(lumière, Projecteur):
        return Instruction_projecteur(lumière, dimmeur, duree, temps_init, synchro)
    elif isinstance(lumière, Led):
        return Instruction_led(lumière, dimmeur, duree, temps_init, synchro, couleur)
    elif isinstance(lumière, Trappe):
        action = dimmeur
        try:
            action = INST_TRAPPE[action]
        except:
            raise(Exception("Erreur trappe : l'instruction {} n'existe pas".format(action)))
        return Instruction_trappe(lumière, action,duree, temps_init, synchro)
    elif isinstance(lumière, Enceintes):
        return Instruction_enceinte(lumière, dimmeur, duree, temps_init, synchro) 

    elif isinstance(lumière, Lyre):
        type_inst = dimmeur
        args = couleur
        if type_inst == "position":
            return Instruction_position(lumière, args, duree, temps_init, synchro)
        elif type_inst == "couleur":
            args = couleur
            return Instruction_couleur(lumière, args, duree, temps_init, synchro)
        elif type_inst == "gobo":
            args = couleur
            return Instruction_gobo(lumière, args, duree, temps_init, synchro)
        elif type_inst == "dimmeur":
            return Instruction_dimmeur(lumière, args, duree, temps_init, synchro)
        elif type_inst == "strombo":
           return Instruction_strombo(lumière, args, duree, temps_init, synchro)
        elif type_inst == "relais":
            return Instruction_lampe(lumière, args, temps_init, synchro)
 
    elif isinstance(lumière, Boule):
        type_inst = dimmeur
        args = couleur
        if type_inst == "program":
            return Instruction_program(lumière, args, duree, temps_init, synchro)
        elif type_inst == "vitesse":
            return Instruction_vitesse(lumière, args, duree, temps_init, synchro)
        elif type_inst == "strombo":
            return Instruction_strombo(lumière, args, duree, temps_init, synchro)
        elif type_inst == "relais":
            return Instruction_lampe(lumière, args, temps_init, synchro)
 
    elif isinstance(lumière, Strombo) or isinstance(lumière, Decoupe):
        type_inst = dimmeur
        args = couleur
        if type_inst == "dimmeur":
            return Instruction_dimmeur(lumière, args, duree, temps_init, synchro)
        elif type_inst == "strombo":
            return Instruction_strombo(lumière, args, duree, temps_init, synchro)
        elif type_inst == "relais":
            return Instruction_lampe(lumière, args, temps_init, synchro)

    elif isinstance(lumière, Lampe):
        return Instruction_lampe(lumière, dimmeur, temps_init, synchro)


    elif isinstance(lumière, Variable):
            type_inst = dimmeur
            args = couleur
            return Instruction_variable(lumière, TYPE_INST[type_inst], args, temps_init, synchro, duree)





    return None

