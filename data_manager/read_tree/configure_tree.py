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
    getter.initialize()

    #print(getter.get_tree())

def get_modes(getter):
    for mode in File_yaml(getter, PATH+"/config.yaml").get("MODES", mandatory = True):
        scenar_init, scenar_end = mode.get("scenario_init"), mode.get("scenario_end")
        current = Mode(mode.get_str("name", mandatory=True), scenar_init, scenar_end)
        getter.get_tree().add_mode(current)
        html = mode.get("html")
        if html:
            for inter in html:
                current.add_inter(inter.get_str("name",mandatory=True))

    

