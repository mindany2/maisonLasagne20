from tree.Tree import Tree
from In_out.Peripheric_manager import Peripheric_manager
from data_manager.utils.Getter import Getter
from data_manager.read_tree.configure_peripherics import config_peripherics
from data_manager.read_tree.configure_tree import config_tree

from In_out.network.Server import Server
"""
Create the tree and Peripheric_manager
"""
tree = Tree()
manager = Peripheric_manager()

getter = Getter(tree, manager)

config_peripherics(getter)
config_tree(getter)

Server(getter).start()


