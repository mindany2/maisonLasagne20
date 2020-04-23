from utils.Data_change.utils.Read import ouvrir, lire
from tree.Preset import Preset
from tree.eclairage.Led import Led
from tree.eclairage.Lampe import Lampe
from tree.scenario.Instruction_led import Instruction_led
from tree.scenario.Instruction_projecteur import Instruction_projecteur
from tree.scenario.Instruction_lampe import Instruction_lampe
from tree.eclairage.Projecteur import Projecteur
from tree.scenario.Scenario import Scenario
from tree.boutons.Bouton_simple import Bouton_simple
from tree.boutons.Bouton_poussoir import Bouton_poussoir
from tree.boutons.html.Bouton_simple_html import Bouton_simple_html
from In_out.Liste_interrupteur import Liste_interrupteur


def get_preset(env, index, nom):
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
                marqueur = ("on" == marqueur)
            else:
                nom_scenar = ligne
                marqueur = (nom_scenar != "eteindre")
            # on créer donc un nv scenar
            scenar = Scenario(nom_scenar, marqueur)
            preset.add_scenar(scenar)
        elif scenar != None:
            scenar.add_inst(get_inst(env,ligne.split("|")))

    # maintenant on lie la liste des boutons html et inters utilisé avec le bon scenario

    compt = 0
    for ligne in lire(ouvrir(env.nom+"/preset/"+nom+"/boutons.data")):
        (vide, nom_bt, type_bt, nom_scenar, mode) = ligne.split("|") 
        if type_bt == "html":
            if mode == "simple":
               scenar = preset.get_scenar(nom_scenar)
               print("scenario "+nom_scenar)
               assert(scenar != None)
               bt = Bouton_simple_html(nom_bt, scenar, (compt, index))
               preset.add_boutons_html(bt)
               compt += 1
        elif type_bt == "inter":
            assert(Liste_interrupteur().get_inter(nom_bt) != None)
            if mode == "poussoir":
               scenar_on = preset.get_scenar(nom_scenar.split(",")[0])
               scenar_off = preset.get_scenar(nom_scenar.split(",")[1])
               assert(scenar_on != None)
               assert(scenar_off != None)
               bt = Bouton_poussoir(nom_bt, env, scenar_on, scenar_off)
               preset.add_lien_inter(nom_bt, bt)



                

    return preset


def get_inst(env, infos):
    """
    Créer une instruction
    """
    nom_lampe = infos[1]
    dimmeur = int(infos[2])
    duree = int(infos[3])
    temps_init = int(infos[4])
    couleur = infos[5]
    try:
        synchro = infos[6] == "oui"
    except:
        synchro = False
    
    lumière = env.get_lumiere(nom_lampe)
    if isinstance(lumière, Projecteur):
        return Instruction_projecteur(lumière, dimmeur, duree, temps_init, synchro)
    elif isinstance(lumière, Led):
        return Instruction_led(lumière, dimmeur, duree, temps_init, synchro, couleur)
    elif isinstance(lumière, Lampe):
        return Instruction_lampe(lumière, dimmeur, temps_init, synchro)
    raise(IOError)

