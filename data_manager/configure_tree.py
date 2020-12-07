from tree.Tree import Tree
from data_manager.configure_environnement import config_environnements

tree = Tree()
PATH = "data/environnements"

def config_tree():
    # Environnements
    config_environnements(tree.get_global_env(), PATH)

    print(tree)

