from In_out.Peripheric_manager import Peripheric_manager
from In_out.external_boards.relay.Relay_GPIO import Relay_GPIO
from In_out.external_boards.relay.Relay_network import Relay_network

manager = Peripheric_manager()

def get_relay(index_relay, board):
    if board == "gpio":
        # the realy index is the gpio port
        return Relay_GPIO(index_relay)
    elif board.count("."):
        # a relay on the network
        rpi_name, board = board.split(".")
        addr = (int(board), int(index_relay))
        return Relay_network(Peripheric_manager().get_connections(rpi_name), addr)
    else:
        # it is a board
        index_board = int(board)
        index_relay = int(index_relay)
        return manager.get_relay(index_board, index_relay)

def get_triak(index_triak, index_board):
    return manager.get_triak(int(index_board), int(index_triak))

def get_addr(addr):
    if addr:
        return addr.replace(")","").split("(")
    return None

def get_dmx():
    return manager.get_dmx()

def get_amp(name):
    return manager.get_amp(name)

