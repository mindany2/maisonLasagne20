from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Secrets import Secrets

from In_out.Peripheric_manager import Peripheric_manager

from In_out.dmx.Wireless_transmitter import Wireless_transmitter
from In_out.dmx.controllers.Dmx_network import Dmx_network
from In_out.dmx.controllers.KingDMX import KingDMX
from In_out.dmx.Wireless_transmitter import Wireless_transmitter

from In_out.external_boards.Board_triak import Board_triak
from In_out.external_boards.relay.Board_relay_extender import Board_relay_extender

from In_out.sound.Amp_6_channels import Amp_6_channels

from In_out.network.Rpi import Rpi
from In_out.network.PC import PC

from In_out.utils.ST_nucleo import ST_nucleo
from In_out.utils.Port_extender import Port_extender

from In_out.sound.spotify.Spotify import Spotify


def config_peripherics(getter):
    """
    Read the config file in data
    to setup the Peripheric_manager
    """
    config = File_yaml(getter, "data/config.yaml")

    # ME
    name = config.get_str("ME", mandatory=True)
    getter.get_manager().set_name(name)

    # BOARDS
    config.get("BOARDS", get_boards)

    #NETWORK
    config.get("NETWORK", get_network)

    #DMX
    config.get("DMX", get_dmx)

    #SOUND
    config.get("SOUND", get_sound)
    #print(getter.get_manager())

def get_sound(sound):
    manager = sound.get_getter().get_manager()
    spotify = sound.get("Spotify")
    if spotify:
        manager.set_spotify(Spotify(spotify.get_str("name", mandatory = True),
                                    Secrets(sound.get_getter()).get_spotify_secret(),
                                    spotify.get_str("pi_id", mandatory = True),
                                    spotify.get("scenar_start"),
                                    spotify.get("scenar_stop"),
                                    spotify.get("scenar_volume"),
                                    spotify.get_int("analysis"),
                                    spotify.get_int("volume_init")))
    amps = sound.get("Amps")
    if amps:
        for amp in amps:
            type_amp = amp.get_str("type", mandatory = True)
            if type_amp == "dax66":
                manager.set_amp(Amp_6_channels(amp.get_str("name", mandatory = True),
                                    amp.get_addr("relay", mandatory = True).get_relay(),
                                    amp.get_str("addr", mandatory = True)))

def get_dmx(dmx):
    manager = dmx.get_getter().get_manager()
    type_dmx = dmx.get_str("type", mandatory = True)
    wireless = dmx.get("wireless")
    list_transmiters = []
    if wireless:
        for transmitter in wireless:
            list_transmiters.append(Wireless_transmitter(transmitter.get_addr("relay").get_relay(),
                                                         transmitter.get_int("mini", mandatory = True),
                                                         transmitter.get_int("maxi", mandatory = True)))
    if type_dmx == "network":
        rpi = manager.get_connection(dmx.get_str("name", mandatory = True))
        manager.set_dmx(Dmx_network(rpi, list_transmiters))
    elif type_dmx == "kingDMX":
        manager.set_dmx(KingDMX(dmx.get_str("addr", mandatory = True), list_transmiters))

def get_network(network_list):
    manager = network_list.get_getter().get_manager()
    for connection in network_list:
        type_con = connection.get_str("type", mandatory = True)
        if type_con == "rpi":
            manager.set_connection(Rpi(connection.get_str("name", mandatory = True),
                                       connection.get_str("ip", mandatory = True),
                                       manager.get_name()))
        elif type_con == "pc":
            manager.set_connection(PC(connection.get_str("name", mandatory = True),
                                      connection.get_str("mac", mandatory = True),
                                      connection.get_str("ip", mandatory = True),
                                      manager.get_name()))

def get_boards(boards):
    boards.get("ST_nucleos", get_st)
    extender = boards.get("Port_extender")
    if extender:
        extender.get("relay_boards", get_relays)

def get_relays(list_boards):
    manager = list_boards.get_getter().get_manager()
    port_extender = Port_extender()
    manager.set_extender(port_extender)
    for board in list_boards:
       index, nb_relay = board.get("index,nb_relay", mandatory = True).split(",", 2)
       addr = board.get_int("addr", mandatory = True)
       index = int(index)
       nb_relay = int(nb_relay)
       manager.set_relay_board(Board_relay_extender(port_extender, index, addr, nb_relay))

def get_st(st_list):
    manager = st_list.get_getter().get_manager()
    for st_config in st_list:
        st = ST_nucleo(st_config.get_str("name", mandatory = True), st_config.get_str("addr", mandatory = True))
        for triak_boards in st_config.get("triak_boards", mandatory = True):
            index, nb_triak = triak_boards.get("index,nb_triak", mandatory = True).split(",", 2)
            # exeption raise if it is not intergers
            index = int(index)
            nb_triak = int(nb_triak)
            st.add_board_triak(Board_triak(index, st, nb_triak))
        manager.set_st_nucleo(st)

