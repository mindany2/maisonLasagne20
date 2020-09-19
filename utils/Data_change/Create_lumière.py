from In_out.cartes.Gestionnaire_de_cartes import Gestionnaire_de_cartes
from In_out.son.Ampli_6_zones import Ampli_6_zones
from tree.eclairage.Led import Led
from tree.utils.Variable import Variable
from tree.eclairage.Enceintes import Enceintes
from tree.eclairage.Lampe import Lampe
from In_out.bluetooth_devices.LEDBLE import LEDBLE
from In_out.bluetooth_devices.ELK_BLEDOM import ELK_BLEDOM
from In_out.bluetooth_devices.TRIONES import TRIONES
from In_out.wifi_devices.LEDnet import LEDnet
from In_out.dmx.Device_dmx import Device_dmx
from In_out.dmx.Controleur_dmx import Controleur_dmx
from tree.eclairage.dmx.Lyre import Lyre
from tree.eclairage.dmx.Boule import Boule
from tree.eclairage.dmx.Laser import Laser
from tree.eclairage.dmx.Strombo import Strombo
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
    if len(specification) > 1:
        option_lumiere = specification[1]
    addr_relais = get_addr(infos[2])
    addr_triac = get_addr(infos[3])
    addr_bluetooth_ou_ip = infos[4]
    
    if addr_triac != None:
        triac = Gestionnaire_de_cartes().get_triac(int(addr_triac[1]), int(addr_triac[0]))
    else:
        triac = None

    if addr_relais != None:
        relais = Gestionnaire_de_cartes().get_relais(addr_relais[1], int(addr_relais[0]))
    else:
        relais = None

    if type_lumière == "projo":
        if option_lumiere == "A63":
            spec = LAMPE.type_63
        elif option_lumiere == "A91":
            spec = LAMPE.type_91
        elif option_lumiere == "A64":
            spec = LAMPE.type_64
        elif option_lumiere == "A73":
            spec = LAMPE.type_73
        elif option_lumiere == "A61":
            spec = LAMPE.type_61
        elif option_lumiere == "A65":
            spec = LAMPE.type_65
        else:
            spec = None
        return Projecteur(nom, triac, spec , relais = relais)

    elif type_lumière == "led":
        if option_lumiere == "triones":
            controleur = TRIONES(addr_bluetooth_ou_ip)
        elif option_lumiere == "ble":
            controleur = LEDBLE(addr_bluetooth_ou_ip)
        elif option_lumiere == "bledom":
            controleur = ELK_BLEDOM(addr_bluetooth_ou_ip)
        elif option_lumiere == "lednet":
            controleur = LEDnet(addr_bluetooth_ou_ip)
        return Led(nom, relais, controleur)
    elif type_lumière == "lampe":
        return Lampe(nom, relais)

    elif type_lumière == "enceinte":
        zone, ampli = get_addr(addr_bluetooth_ou_ip)
        if ampli == "dax66":
            zone = Ampli_6_zones.get_zone(int(zone))
            if not(zone):
                raise(Exception("Il y a des enceintes sans ampli"))
            return Enceintes(nom, Ampli_6_zones, zone)

    elif type_lumière == "lyre":
        return Lyre(nom, Device_dmx(Controleur_dmx(), int(addr_bluetooth_ou_ip)))
    elif type_lumière == "boule":
        return Boule(nom, Device_dmx(Controleur_dmx(), int(addr_bluetooth_ou_ip)))
    elif type_lumière == "strombo":
        return Strombo(nom, Device_dmx(Controleur_dmx(), int(addr_bluetooth_ou_ip)))

    elif type_lumière == "variable":
        return Variable(nom, int(addr_bluetooth_ou_ip))


            





