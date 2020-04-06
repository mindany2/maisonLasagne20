from utils.Data_change.utils.Read import ouvrir, lire
from tree.Preset import Preset
from tree.eclairage.Led import Led
from tree.scenario.Instruction_led import Instruction_led
from tree.scenario.Instruction_projecteur import Instruction_projecteur
from tree.eclairage.Projecteur import Projecteur
from tree.scenario.Scenario import Scenario


def get_preset(env, nom):
    """
    On recupére la preset
    """
    preset = Preset(nom)
    scenar = None
    for ligne in lire(ouvrir(env.nom+"/preset/"+nom)):
        if ligne.count("|") == 0:
            scenar = Scenario(ligne)
            preset.add_scenar(scenar)
        elif scenar != None:
            scenar.add_inst(get_inst(env,ligne.split("|")))
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
    
    print(nom_lampe)
    lumière = env.get_lumiere(nom_lampe)
    if isinstance(lumière, Projecteur):
        return Instruction_projecteur(lumière, dimmeur, duree, temps_init, synchro)
    elif isinstance(lumière, Led):
        return Instruction_led(lumière, dimmeur, duree, temps_init, synchro, couleur)
    raise(IOError)

