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

def config_environnements(getter, env, path, name_env = "global"):
    """
    Configure an environnement
    """
    # Sub-env
    for sub_env in list_folders(path):
        if sub_env != "presets":
            envi = Environnement(sub_env)
            env.add_env(envi)
            config_environnements(getter, envi, path+"/"+sub_env, name_env+"."+sub_env)

    config = File_yaml(getter, path+"/"+CONFIG_FILE)

    # Variables
    config.get("Variables", get_variables, args=env)

    # Objects
    config.get("Objects", get_objects, args = env)

    # Network interrupt
    config.get("Interrupts", get_network_inter, args = name_env)

    # Presets
    get_presets(getter, env, path+"/presets")

    # Modes
    config.get("Modes", get_modes, args = env)

def get_network_inter(inters, name_env):
    getter = inters.get_getter()
    for inter in Csv_reader(getter, inters.get("config", mandatory=True)):
        name, type_inter, args = inter.get_str("name"), inter.get_str("type"), inter.get("args")
        if type_inter == "network":
            try:
                connection = getter.get_manager().get_connection(str(args))
            except KeyError:
                args.raise_error("Could not find connection {}".format(str(args)))
            connection.add_input_interrupt(name, name_env)

def get_modes(modes, env):
    getter = modes.get_getter()
    for link in modes:
        mode, preset = link.get_str("mode", mandatory = True), link.get_str("preset", mandatory = True)
        try:
            getter.get_mode(mode)
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
    try:
        for spotify_var in variables.get_getter().get_manager().get_spotify().get_variables():
            env.add_variable(spotify_var, recursive=False)
    except NameError:
        pass
    env.add_variable(Variable_env(variables.get_getter().get_tree()), recursive=False)
    for var in variables:
        env.add_variable(Variable(var.get_str("name", mandatory = True),
                                  var.get_int("value", mandatory = True)))

        




