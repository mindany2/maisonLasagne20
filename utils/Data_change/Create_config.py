from In_out.interruptions.Gestionnaire_interruptions import Gestionnaire_interruptions
from In_out.cartes.Gestionnaire_de_cartes import Gestionnaire_de_cartes
from In_out.interruptions.inter.Interruption import TYPE_INTER
from In_out.interruptions.Liste_interruptions_extender import Liste_interruptions_extender
from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Carte_relais_extender import Carte_relais_extender
from In_out.utils.ST_nucleo import ST_nucleo
from In_out.son.Ampli_6_zones import Ampli_6_zones
from In_out.dmx.Controleur_dmx import Controleur_dmx
from utils.Data_change.utils.Read import ouvrir, lire
from utils.spotify.Spotify import Spotify
from utils.Logger import Logger
from tree.Tree import Tree

def get_config_music():
    # configure spotify
    Spotify().init()
    mode = ""
    for ligne in lire(ouvrir("config.data", False)):
        if ligne.count("---") != 0:
            mode = ligne.split("---")[1]
            continue

        if mode == "spotify":
            nom, arg = ligne.split("=")
            if nom == "analysis":
                Spotify().ANALYSIS = (arg == "oui")
            elif nom == "pi_id":
                Spotify.set_pi_id(arg)
            elif nom == "start":
                env, preset, scenar = arg.split(".")
                print(Tree().get_env(env).get_preset(preset).get_scenar(scenar))
                Spotify().set_scenar_start(Tree().get_env(env).get_preset(preset).get_scenar(scenar))
            elif nom == "stop":
                env, preset, scenar = arg.split(".")
                Spotify().set_scenar_stop(Tree().get_env(env).get_preset(preset).get_scenar(scenar))
            elif nom == "reload":
                env, preset, scenar = arg.split(".")
                Spotify().set_scenar_reload(Tree().get_env(env).get_preset(preset).get_scenar(scenar))



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

                liste = Liste_interruptions_extender(port, port_bus, registre)

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

        if mode == "stnucleo":
            st_addr = ligne.split("=")[1]
            st_nucleo = ST_nucleo(st_addr)


        elif mode == "ampli":
            type_ampli, args = ligne.split("=")
            addr, relais = args.split(",")

            if (type_ampli == "dax66"):
                relais = Gestionnaire_de_cartes.get_relais(relais[2], relais[0])

                if not(relais):
                    Logger.error("Definir d'abord les cartes avant l'ampli")
                    continue

                Ampli_6_zones.init(addr, relais)

        elif mode == "dmx":
            null, addr = ligne.split("=")
            Controleur_dmx().init(addr)

        elif mode == "cartes":
            if not(st_nucleo):
                Logger.error("Pas de carte ST")
                Logger.warn("Veuillez la definir avant les cartes")
                continue

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
                    carte = Carte_relais_extender(numero,port_bus,nb_ports)
                else:
                    raise("TODO")
            elif carte == "triac":
                if type_conn != "st_nucleo":
                    raise("Les triacs ne fonctionne que sur la st")
                carte = Carte_triac(numero, st_nucleo) # les cartes ont tjrs 8 triacs

            else:
                raise("Type de carte inconnu")
            Gestionnaire_de_cartes.configure(carte)
