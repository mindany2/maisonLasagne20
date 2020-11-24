from utils.Data_change.Create_lumière import get_relais, get_addr
from In_out.interruptions.Gestionnaire_interruptions import Gestionnaire_interruptions
from In_out.Gestionnaire_peripheriques import Gestionnaire_peripheriques
from In_out.interruptions.inter.Interruption import TYPE_INTER
from In_out.interruptions.Liste_interruptions_extender import Liste_interruptions_extender
from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Carte_relais_extender import Carte_relais_extender
from In_out.utils.ST_nucleo import ST_nucleo
from In_out.communication.Rpi import Rpi
from In_out.communication.PC import PC
from In_out.utils.Port_extender import Port_extender
from In_out.son.Ampli_6_zones import Ampli_6_zones
from In_out.dmx.controleurs.KingDMX import KingDMX
from In_out.dmx.controleurs.RpiDMX import RpiDMX
from In_out.dmx.Transmetteur import Transmetteur
from utils.Data_change.utils.Read import ouvrir, lire
from utils.spotify.Spotify import Spotify
from utils.Logger import Logger
from tree.Tree import Tree

def get_config_music():
    # configure spotify
    mode = ""
    for ligne in lire(ouvrir("config.data", False)):
        if ligne.count("---") != 0:
            mode = ligne.split("---")[1]
            continue

        if mode == "spotify":
            nom, arg = ligne.split("=")
            if nom == "analysis":
                Spotify.ANALYSIS = (arg == "oui")
            elif nom == "pi_id":
                Spotify.set_pi_id(arg)
            elif nom == "start":
                env, preset, scenar = arg.split(".")
                Spotify().set_scenar_start(Tree().get_env(env).get_preset(preset).get_scenar(scenar))
            elif nom == "stop":
                env, preset, scenar = arg.split(".")
                Spotify().set_scenar_stop(Tree().get_env(env).get_preset(preset).get_scenar(scenar))
            elif nom == "reload":
                env, preset, scenar = arg.split(".")
                Spotify().set_scenar_reload(Tree().get_env(env).get_preset(preset).get_scenar(scenar))

    Spotify().init()


def get_config_inter():
    # lis la configuration des interruptions pour remplir Gestionnaire_interruptions
    mode = ""
    Gestionnaire_interruptions.init()

    for ligne in lire(ouvrir("config.data", False)):

        if ligne.count("---") != 0:
            mode = ligne.split("---")[1]
            print(mode)
            continue

        if mode == "interrupt":
            # interruptions
            port, type_inter, args = ligne.split("|")

            try:
                port = int(port)
            except:
                raise("Erreur dans le fichier de config : le port n'est pas entier")

            if type_inter=="extender":
                try:
                    port_bus, registre = args.split(",")
                    port_bus = int(port_bus,16) # en hexa
                    registre = int(registre)
                except:
                    raise("Erreur dans le fichier de config : les arguments de l'extender ne sont pas valide")

                liste = Liste_interruptions_extender(Gestionnaire_interruptions().get_extender(), port, port_bus, registre)

                Gestionnaire_interruptions().configure(liste, TYPE_INTER.extender)

            elif type_inter == "gpio":
                Logger.warn("pas besoin de configurer les gpios")


def get_config_carte():
    # lit la config des différentes cartes relais et triac avec lequel le rpi peut communiquer
    mode = ""
    
    for ligne in lire(ouvrir("config.data", False)):

        if ligne.count("---") != 0:
            mode = ligne.split("---")[1]
            continue

        if mode == "connections":
            nom, type_com, args = ligne.split("=")[1].split(",")
            com = None
            if type_com == "rpi":
                com = Rpi(nom, addr)
            elif type_com == "pc":
                addr_ip, addr_mac, = args.split("/")
                com = PC(nom, addr_mac.replace(".",":"), addr_ip)
            Gestionnaire_peripheriques().configure(com)

        if mode == "stnucleos":
            st_nom, st_addr, decal = ligne.split("=")[1].split(",")
            Gestionnaire_peripheriques().configure(ST_nucleo(st_nom, st_addr, int(decal)))

        if mode == "extender":
            Gestionnaire_peripheriques().configure(Port_extender())

        elif mode == "ampli":
            type_ampli, args = ligne.split("=")
            addr, relais = args.split(",")

            if (type_ampli == "dax66"):
                relais = get_relais(get_addr(relais))

                if not(relais):
                    Logger.error("Definir d'abord les cartes avant l'ampli")
                    continue

                Ampli_6_zones.init(addr, relais)

        elif mode == "dmx":
            vals = ligne.split("=")[1].split(",")
            type_dmx, addr = vals[0], vals[1]
            dmx = None
            transmetter = None
            if len(vals) > 2:
                addr_relais, mini, maxi = vals[2].split("/")
                relais = get_relais(get_addr(addr_relais))
                transmetter = Transmetteur(relais, int(mini), int(maxi))
            if type_dmx == "kingDMX":
                dmx = KingDMX(addr, transmetter)
            elif type_dmx == "rpiDMX":
                dmx = RpiDMX(Gestionnaire_peripheriques().get_connections(addr))
            Gestionnaire_peripheriques.configure(dmx)

        elif mode == "cartes":
            numero, carte, type_conn , nb_ports, args = ligne.split("|")

            try:
                numero = int(numero)
                nb_ports = int(nb_ports)
            except:
                raise("Erreur dans le fichier de config : le numero ou le nb de ports n'est pas entier")
            if carte == "relais":
                if type_conn == "extender":
                    try:
                        port_bus = int(args,16)
                    except:
                        raise("Erreur dans le fichier de config : le port_bus n'est pas entier")
                    carte = Carte_relais_extender(Gestionnaire_peripheriques().get_extender(), numero,port_bus,nb_ports)
                else:
                    raise("TODO")
            elif carte == "triac":
                carte = Carte_triac(numero, Gestionnaire_peripheriques().get_st_nucleo(type_conn)) # les cartes ont tjrs 8 triacs

            else:
                raise("Type de carte inconnu")
            Gestionnaire_peripheriques.configure(carte)
