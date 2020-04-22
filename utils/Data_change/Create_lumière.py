from In_out.cartes.Gestionnaire_de_cartes import Gestionnaire_de_cartes
from tree.eclairage.Led import Led
from tree.eclairage.Lampe import Lampe
from In_out.bluetooth_devices.Controleur_4_pins import Controleur_4_pins
from In_out.bluetooth_devices.Controleur_5_pins import Controleur_5_pins
from tree.eclairage.Projecteur import Projecteur, LAMPE

def get_addr(addr):
    if addr != "":
        return addr.replace(")","").split("(")
    return None

def get_lumiere(infos):
    """
    Créer la lumière correspondante avec les bonnes infos
    """
    nom = infos[0]
    specification = infos[1].split("_")
    type_lumière = specification[0]
    option_lumiere = specification[1]
    addr_relais = get_addr(infos[2])
    addr_triac = get_addr(infos[3])
    addr_bluetooth = infos[4]
    
    if addr_triac != None:
        triac = Gestionnaire_de_cartes().get_triac(int(addr_triac[1]), int(addr_triac[0]))
    else:
        triac = None

    if addr_relais != None:
        relais = Gestionnaire_de_cartes().get_relais(int(addr_relais[1]), int(addr_relais[0]))
    else:
        relais = None

    if type_lumière == "projo":
        if option_lumiere == "plafond":
            spec = LAMPE.type_plafond
        elif option_lumiere == "poutres":
            spec = LAMPE.type_poutre
        else:
            spec = None
        return Projecteur(nom, triac, spec , relais = relais)

    elif type_lumière == "led":
        if option_lumiere == "2":
            controleur = Controleur_4_pins(addr_bluetooth)
        elif option_lumiere == "1":
            controleur = Controleur_5_pins(addr_bluetooth)
        return Led(nom, relais, controleur)
    elif type_lumière == "lampe":
        return Lampe(nom, relais)
