from tree.Mode import Mode
from data_manager.read_tree.configure_environnement import config_environnements
from data_manager.utils.File_yaml import File_yaml


PATH = "data"

def config_tree(getter):
    # Modes
    get_modes(getter)

    # Environnements
    config_environnements(getter, getter.get_tree().get_global_env(), PATH + "/environnements")

    # Initialize 
    getter.get_tree().initialize()

    #print(getter.get_tree())

def get_modes(getter):
    for mode in File_yaml(getter, PATH+"/config_tree.yaml").get("MODES", mandatory = True):
        scenar_init = mode.get("scenar_init")
        getter.get_tree().add_mode(Mode(mode.get_str("name"), scenar_init))

    

