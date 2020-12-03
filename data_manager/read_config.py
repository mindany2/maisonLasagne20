from data_manager.utils.File_yaml import File_yaml
from data_manager.read_object import get_relay
from data_manager.utils.utils import get_int

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

from In_out.spotify.Spotify import Spotify

manager = Peripheric_manager()

def config_peripherics():
    """
    Read the config file in data
    to setup the Peripheric_manager
    """
    config = File_yaml("data/config.yaml")

    # BOARDS
    config.get("BOARDS", get_boards)

    #NETWORK
    config.get("NETWORK", get_network)

    #DMX
    config.get("DMX", get_dmx)

    #SOUND
    config.get("SOUND", get_sound)

def get_sound(sound):
    spotify = sound.get("Spotify")
    if spotify:
        manager.set_spotify(Spotify(spotify.get("name"),
                                    spotify.get("pi_id"),
                                    spotify.get("scenar_start"),
                                    spotify.get("scenar_stop"),
                                    spotify.get("scenar_volume"),
                                    spotify.get("analysis"),
                                    get_int(spotify.get("volume_init"))))
    amps = sound.get("Amps")
    if amps:
        for amp in amps:
            type_amp = amp.get("type")
            if type_amp == "dax66":
                manager.set_amp(Amp_6_channels(amp.get("name"),
                                    amp.get("addr"),
                                    get_relay(amp.get("relay"))))

def get_dmx(dmx):
    type_dmx = dmx.get("type")
    wireless = dmx.get("wireless")
    list_transmiters = []
    if wireless:
        for transmitter in wireless:
            exception = TypeError("One of the args of the transmitter {} is not an int".format(transmitter))
            list_transmiters.append(Wireless_transmitter(get_relay(transmitter.get("relay")),
                                                         get_int(transmitter.get("mini"),exception),
                                                         get_int(transmitter.get("maxi"), exception)))
    if type_dmx == "network":
        rpi = manager.get_connections(dmx.get("name"))
        manager.set_dmx(Dmx_network(rpi, list_transmiters))
    elif type_dmx == "kingDMX":
        manager.set_dmx(KingDMX(dmx.get("addr"), list_transmiters))

def get_network(network_list):
    for connection in network_list:
        type_con = connection.get("type")
        if type_con == "rpi":
            manager.set_connection(Rpi(connection.get("name"), connection.get("ip")))
        elif type_con == "pc":
            manager.set_connection(PC(connection.get("name"), connection.get("mac"), connection.get("ip")))

def get_boards(boards):
    boards.get("ST_nucleos", get_st)
    extender = boards.get("Port_extender")
    if extender:
        extender.get("relay_boards", get_relays)

def get_relays(list_boards):
    port_extender = Port_extender()
    manager.set_extender(port_extender)
    for board in list_boards:
       index, nb_relay = board["index,nb_relay"].split(",")
       # exeption raise if it is not intergers
       exeption = TypeError("The config of relay board {} in the extender is not interger".format(index))
       addr = get_int(board["addr"], exeption)
       index = get_int(index, exeption)
       nb_relay = get_int(nb_relay, exeption)
       manager.set_relay_board(Board_relay_extender(port_extender, index, addr, nb_relay))

def get_st(st_list):
    for st_config in st_list:
        st = ST_nucleo(st_config.get("name"), st_config.get("addr"))
        for triak_boards in st_config.get("triak_boards"):
            index, nb_triak = triak_boards["index,nb_triak"].split(",")
            # exeption raise if it is not intergers
            exeption = TypeError("The config of triak board {} in the st_nucleo {} is not interger".format(index, st_config.get("name")))
            index = get_int(index, exeption)
            nb_triak = get_int(nb_triak, exeption)
            st.add_board_triak(Board_triak(index, st, nb_triak))
        manager.set_st_nucleo(st)

if __name__ == "__main__":
    config_peripherics()

