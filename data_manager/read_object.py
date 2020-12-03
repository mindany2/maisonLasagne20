from In_out.Peripheric_manager import Peripheric_manager
from In_out.external_boards.relay.Relay_GPIO import Relay_GPIO
from In_out.external_boards.relay.Relay_network import Relay_network

def get_relay(addr_relay):
    addr_relay = get_addr(addr_relay)
    if addr_relay != None:
        board, index_relay = addr_relay[1], addr_relay[0]
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
            return Peripheric_manager().get_relay(index_board, index_relay)
    return None

def get_addr(addr):
    if addr:
        return addr.replace(")","").split("(")
    return None

