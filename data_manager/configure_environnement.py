from data_manager.configure_object import get_objects
from data_manager.configure_preset import get_presets

from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader

from tree.utils.calculs.Variable import Variable 

CONFIG_FILE = "config.yaml"

def config_environnements(env, path):
    """
    Configure an environnement
    """
    config = File_yaml(path+"/"+CONFIG_FILE)

    # Variables
    config.get("Variables", get_variables, args= env)

    # Objects
    config.get("Objects", get_objects, args = env)

    # Presets
    get_presets(env, path+"/presets")

def get_variables(variables, *args):
    env = args[0]
    variables = Csv_reader(variables.get("config"))
    for var in variables:
        env.add_variable(Variable(var.get_str("name", mandatory = True),
                                  var.get_int("value", mandatory = True)))

        




