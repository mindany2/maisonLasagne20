from data_manager.read_tree.configure_object import get_objects
from data_manager.read_tree.configure_preset import get_presets

from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.utils.file_manager import list_folders

from tree.utils.calculs.Variable import Variable 
from tree.utils.calculs.Variable_env import Variable_env
from tree.utils.calculs.Variable_spotify import Variable_spotify

from tree.Environnement import Environnement

CONFIG_FILE = "config.yaml"

def config_environnements(getter, env, path):
    """
    Configure an environnement
    """
    # Sub-env
    for sub_env in list_folders(path):
        if sub_env != "presets":
            envi = Environnement(sub_env)
            env.add_env(envi)
            config_environnements(getter, envi, path+"/"+sub_env)

    config = File_yaml(getter, path+"/"+CONFIG_FILE)

    # Variables
    config.get("Variables", get_variables, args=env)

    # Objects
    config.get("Objects", get_objects, args = env)

    # Presets
    get_presets(getter, env, path+"/presets")

    # Modes
    config.get("Modes", get_modes, args = env)

def get_modes(modes, env):
    getter = modes.get_getter()
    for link in modes:
        mode, preset = link.get_str("mode", mandatory = True), link.get_str("preset", mandatory = True)
        try:
            mode = getter.get_mode(mode)
        except (KeyError, ValueError):
            link.raise_error("Undefine mode {}".format(mode))
        try:
            preset = getter.get_preset(env, preset)
        except (KeyError, ValueError):
            link.raise_error("Undefine preset {}".format(mode))
        env.add_mode(mode, preset)

def get_variables(variables, *args):
    env = args[0]
    variables = Csv_reader(variables.get_getter(), variables.get("config"))
    env.add_variable(Variable_spotify())
    env.add_variable(Variable_env(variables.get_getter()))
    for var in variables:
        env.add_variable(Variable(var.get_str("name", mandatory = True),
                                  var.get_int("value", mandatory = True)))

        




