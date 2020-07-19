from In_out.interruptions.Gestionnaire_interruptions import Gestionnaire_interruptions
from In_out.cartes.Gestionnaire_de_cartes import Gestionnaire_de_cartes
from In_out.interruptions.inter.Interruption import TYPE_INTER
from In_out.interruptions.Liste_interruptions_extender import Liste_interruptions_extender
from In_out.cartes.Carte_triac import Carte_triac
from In_out.cartes.relais.Carte_relais import Carte_relais
from In_out.cartes.relais.Carte_relais_extender import Carte_relais_extender
from In_out.utils.ST_nucleo import ST_nucleo
from utils.Data_change.utils.Read import ouvrir, lire

def get_config_inter():
    # lis la configuration des interruptions pour remplir Gestionnaire_interruptions
    mode = ""
    Gestionnaire_interruptions.init()

    for ligne in lire(ouvrir("config.data", False)):

        if get_mode(ligne) != None:
            mode = get_mode(ligne)
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


def get_config_carte():
    # lit la config des différentes cartes relais et triac avec lequel le rpi peut communiquer
    mode = ""
    
    st_addr = get_st_adresse()

    if st_addr:
        st_nucleo = ST_nucleo(st_addr)
    else:
        print("pas de carte ST")

    for ligne in lire(ouvrir("config.data", False)):

        if get_mode(ligne) != None:
            mode = get_mode(ligne)
            continue

        if mode == "cartes":
            numero, carte, type_conn , nb_ports, args = ligne.split("|")

            try:
                numero = int(numero)
                nb_ports = int(nb_ports)
            except:
                raise("Erreur dans le fichier de config : le numero ou le nb de ports n'est pas entier")
            if carte == "relais":
                print("relias !!!!")
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

def get_st_adresse():
    # on va chercher l'adresse le la st nucleo
    mode = ""

    for ligne in lire(ouvrir("config.data", False)):

        if get_mode(ligne) != None:
            mode = get_mode(ligne)
            continue

        if mode == "stnucleo":
            return ligne.split("=")[1]

    return None


def get_mode(ligne):
    if ligne.count("interrupt"):
         return "interrupt"
    elif ligne.count("cartes"):
         return "cartes"
    elif ligne.count("stnucleo"):
        return "stnucleo"
    return None
