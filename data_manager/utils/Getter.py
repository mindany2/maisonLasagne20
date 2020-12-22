from In_out.external_boards.relay.Relay_GPIO import Relay_GPIO
from In_out.external_boards.relay.Relay_network import Relay_network

import re
class Getter:
    """
    Allow to acces quickly to the tree and manager
    """
    def __init__(self, tree, manager):
        self.tree = tree
        self.manager = manager

    def initialize(self):
        self.tree.initialize()
        self.manager.initialize()

    def get_tree(self):
        return self.tree

    def get_manager(self):
        return self.manager

    def reload_tree(self, tree):
        self.tree = tree

    def get_relay(self, index_relay, board):
        if board == "gpio":
            # the realy index is the gpio port
            return Relay_GPIO(index_relay)
        elif board.count("."):
            # a relay on the network
            rpi_name, board = board.split(".")
            addr = (int(board), int(index_relay))
            return Relay_network(self.manager.get_connection(rpi_name), addr)
        else:
            # it is a board
            index_board = int(board)
            index_relay = int(index_relay)
            return self.manager.get_relay(index_board, index_relay)

    def get_triak(self, index_triak, index_board):
        return self.manager.get_triak(int(index_board), int(index_triak))

    def get_object(self, env, name):
        return env.get_object(name)

    def get_var(self, env, name):
        return env.get_var(name)

    def get_addr(self, addr):
        if addr:
            match = re.match(r'(?P<index>([^\(]*))\((?P<board>([^\)]*))\)', addr)
            if match:
                return [match.group("index"),match.group("board")]
        return None

    def get_scenario(self, preset, name_scenars):
        return [preset.get_scenar(name_scenar) for name_scenar in name_scenars]

    def get_env(self, name_env):
        return self.tree.get_env(name_env)

    def get_preset(self, env, name_preset):
        return env.get_preset(name_preset)

    def get_mode(self, name):
        return self.tree.get_mode(name)

    def get_connection(self, name):
        return self.manager.get_connection(name)

    def get_spotify(self):
        return self.manager.get_spotify()

    def get_dmx(self):
        return self.manager.get_dmx()

    def get_amp(self, name):
        return self.manager.get_amp(name)

