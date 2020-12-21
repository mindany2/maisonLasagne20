from In_out.Gestionnaire_peripheriques import Gestionnaire_peripheriques
from In_out.son.Ampli_6_zones import Ampli_6_zones
from tree.eclairage.Led import Led
from tree.utils.Variable import Variable
from tree.eclairage.Enceintes import Enceintes
from tree.eclairage.Lampe import Lampe
from tree.eclairage.Trappe import Trappe
from In_out.bluetooth_devices.LEDBLE import LEDBLE
from In_out.bluetooth_devices.ELK_BLEDOM import ELK_BLEDOM
from In_out.bluetooth_devices.TRIONES import TRIONES
from In_out.wifi_devices.LEDnet import LEDnet
from In_out.dmx.Device_dmx import Device_dmx
from In_out.capteurs.Capteur_GPIO import Capteur_GPIO
from tree.eclairage.dmx.Lyre import Lyre
from tree.eclairage.dmx.Boule import Boule
from tree.eclairage.dmx.Laser import Laser
from tree.eclairage.dmx.Strombo import Strombo
from tree.eclairage.dmx.Decoupe import Decoupe
from tree.eclairage.Projecteur import Projecteur, LAMPE
from In_out.cartes.relais.Relais_GPIO import Relais_GPIO
from In_out.cartes.relais.Relais_rpi import Relais_rpi

def get_relais(addr_relais):
    if addr_relais != None:
        carte, indice_relais = addr_relais[1], addr_relais[0]
        if carte == "gpio":
            # l'indice du relais joue le role du port gpio
            return Relais_GPIO(indice_relais)
        elif carte.count(","):
            # relais rpi
            rpi, carte = carte.split(",")
            addr = (int(carte), int(indice_relais))
            return Relais_rpi(Gestionnaire_peripheriques().get_connections(rpi), addr)
        else:
            # c'est une carte
            indice_carte = int(carte)
            indice_relais = int(indice_relais)
            return Gestionnaire_peripheriques().get_relais(indice_carte, indice_relais)
    return None

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
        elif option_lumiere == "A200":
            spec = LAMPE.type_200
        else:
            spec = None
        
        if addr_triac != None:
            triac = Gestionnaire_peripheriques().get_triac(int(addr_triac[1]), int(addr_triac[0]))
        else:
            triac = None

        relais = get_relais(addr_relais)
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
        relais = get_relais(addr_relais)
        return Led(nom, relais, controleur)
    elif type_lumière == "lampe":
        relais = get_relais(addr_relais)
        return Lampe(nom, relais)

    elif type_lumière == "enceinte":
        zone, ampli = get_addr(addr_bluetooth_ou_ip)
        if ampli == "dax66":
            zone = Ampli_6_zones.get_zone(int(zone))
            if not(zone):
                raise(Exception("Il y a des enceintes sans ampli"))
            return Enceintes(nom, Ampli_6_zones, zone)

    elif type_lumière == "lyre":
        relais = get_relais(addr_relais)
        return Lyre(nom, relais, Device_dmx(Gestionnaire_peripheriques().get_dmx(), int(addr_bluetooth_ou_ip)))
    elif type_lumière == "boule":
        relais = get_relais(addr_relais)
        return Boule(nom, relais, Device_dmx(Gestionnaire_peripheriques().get_dmx(), int(addr_bluetooth_ou_ip)))
    elif type_lumière == "strombo":
        relais = get_relais(addr_relais)
        return Strombo(nom, relais, Device_dmx(Gestionnaire_peripheriques().get_dmx(), int(addr_bluetooth_ou_ip)))
    elif type_lumière == "decoupe":
        relais = get_relais(addr_relais)
        return Decoupe(nom, relais, Device_dmx(Gestionnaire_peripheriques().get_dmx(), int(addr_bluetooth_ou_ip)))

    elif type_lumière == "variable":
        return Variable(nom, int(addr_bluetooth_ou_ip))

    elif type_lumière == "trappe":
        monte, descend, aimant, capteur = get_addr(infos[2]), get_addr(infos[3]), get_addr(infos[4]), get_addr(infos[5])
        relais_monte = get_relais(monte)
        relais_descend = get_relais(descend)
        relais_aimant = get_relais(aimant)
        if capteur[1] == "gpio":
            capteur_trappe = Capteur_GPIO("Capteur Trappe",int(capteur[0]))
        return Trappe(nom, relais_monte, relais_descend, relais_aimant, capteur_trappe)


            





