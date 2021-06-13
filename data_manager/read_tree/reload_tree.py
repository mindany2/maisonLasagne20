from tree.Tree import Tree
from data_manager.utils.Getter import Getter
from data_manager.read_tree.configure_tree import config_tree, PATH
from tree.utils.Dico import Dico
import sys
from enum import Enum

def reload_tree(old_getter, path = PATH):
    """
    Manage to reload all the tree to change environnements, scenarios, light..
    Without shutdown all the process
    //!\\ did not change the peripheric manager
    """
    sys.setrecursionlimit(1500)
    manager = old_getter.get_manager()
    old_tree = old_getter.get_tree()
    new_getter = Getter(Tree(), manager)
    config_tree(new_getter, path=path)
    new_tree = new_getter.get_tree()

    # we have the old tree and the new one created

    # reload all the envs
    reload_env(new_tree.get_global_env(), old_tree.get_global_env())

    # reload mode selected
    old_mode = old_tree.get_current_mode()
    new_tree.change_mode(old_mode.name)

    old_getter.reload_tree(new_tree)

    new_tree.do_current_scenars()


def reload_env(new_env, old_env):
    # parkour all the env
    for new_sub_env in new_env.get_list_subs_env():
        try:
            old_sub_env = old_env.get_list_subs_env().get(new_sub_env.name)
            reload_env(new_sub_env, old_sub_env)
        except KeyError:
            pass

    # parkour all the objects
    for new_obj in new_env.get_list_objs():
        try:
            old_obj = old_env.get_list_objs().get(new_obj.name)
            new_obj.reload(old_obj)
        except KeyError:
            pass

    # parkour all the preset
    for new_preset in new_env.get_list_presets():
        try:
            old_preset = old_env.get_list_presets().get(new_preset.name)
            reload_preset(new_preset, old_preset)
        except KeyError:
            pass

    # reload variables
    new_calculator, old_calculator = new_env.get_calculator(), old_env.get_calculator()
    for new_variable in new_calculator.get_list_variables():
        try:
            old_variable = old_calculator.get(new_variable.name)
            new_variable.reload(old_variable)
        except KeyError:
            pass
    
def reload_preset(new_preset, old_preset):
    new_preset.reload(old_preset)

    # reload manager
    new_manager, old_manager = new_preset.get_manager(), old_preset.get_manager()
    reload_scenario_manager(new_manager, old_manager, new_preset.get_list_scenars())

    # reload scenar
    for new_scenar in new_preset.get_list_scenars():
        try:
            old_scenar = old_preset.get_list_scenars().get(new_scenar.name)
            new_scenar.reload(old_scenar)
        except KeyError:
            pass

def reload_scenario_manager(new_manager, old_manager, list_scenar):
    # scenar selected
    old_scenar_select = old_manager.get_scenar_select()
    if old_scenar_select:
        try:
            new_scenar_selected = list_scenar.get(old_scenar_select.name)
            new_manager.reload_scenar_selected(new_scenar_selected)
        except KeyError:
            pass

    #current scenar
    old_current_scenar = old_manager.get_current_scenar()
    if old_current_scenar:
        try:
            new_scenar_selected = list_scenar.get(old_current_scenar.name)
            new_manager.reload_current_scenar(new_scenar_selected)
        except KeyError:
            pass

    # stack
    #TODO check if the stack is in the order
    for scenar in old_manager.get_stack():
        try:
            new_scenar = list_scenar.get(scenar.name)
            new_manager.push(new_scenar)
        except KeyError:
            pass




