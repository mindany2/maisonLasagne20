from data_manager.utils.file_manager import list_files
from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.read_tree.configure_instructions import get_instructions

from tree.Preset import Preset

from tree.scenario.Scenario import Scenario, MARKER
from tree.buttons.Button_principal import Button_principal
from tree.buttons.Button_secondary import Button_secondary
from tree.buttons.Button_choice import Button_choice


def get_presets(getter, env, path):
    for preset_yaml in list_files(path):
        name = preset_yaml.split(".")[0]
        file = File_yaml(getter, "{}/{}".format(path, preset_yaml))
        preset = Preset(name)

        # Scenarios
        file.get("Scenarios", get_scenarios, args = [preset, env])

        # Interrupts Button
        interrupts = file.get("Interrupts")
        if interrupts:
            interrupts.get("buttons", get_buttons, args = [preset, env], mandatory = True)

        # HTML Button
        html = file.get("HTML")
        if html:
            html.get("buttons", get_buttons, args = [preset, env])

        env.add_preset(preset)


def get_buttons(buttons, args):
    preset, env = args
    try:
        manager = preset.get_manager()
    except ValueError as e:
        buttons.raise_error(str(e))

    getter = buttons.get_getter()

    for inter in Csv_reader(getter, buttons):
        name, type_bt, scenars = inter.get_str("name"), inter.get("type"), inter.get("scenarios")
        list_scenar = []
        for scenar in scenars.split(","):
            try:
                list_scenar.append(preset.get_scenar(str(scenar)))
            except KeyError:
                scenar.raise_error("Could not found scenario {} in preset {}".format(str(scenar), preset.name))
        preset.add_button(get_bt(name, manager, type_bt, list_scenar))

def get_bt(name, manager, type_bt, list_scenar):
        if str(type_bt) == "principal":
            scenar2 = None
            if len(list_scenar) > 1:
                scenar2 = list_scenar[1]
            return Button_principal(name, manager, list_scenar[0], scenar2)
        elif str(type_bt) == "secondary":
            return Button_secondary(name, manager, list_scenar[0])
        elif str(type_bt) == "choice":
            return Button_choice(name, manager, list_scenar)
        else:
            type_bt.raise_error("Could not find a button type {}".format(str(type_bt)))

def get_scenarios(scenarios, args):
    preset, env = args
    for scenar in scenarios:
        name = scenar.get_str("name", mandatory = True)
        loop = scenar.get_int("loop")
        if not(loop): loop = False
        marker = scenar.get("marker", mandatory = True)
        if marker:
            try:
                type_marker = MARKER[str(marker)]
            except KeyError:
                marker.raise_error("The marker {} does not exist in Scenario.py".format(str(marker)))
        scenario = Scenario(name, type_marker, env.get_calculator(), loop)

        # Instructions
        scenar.get("instructions", get_instructions, args = [env, scenario], mandatory = True)

        preset.add_scenar(scenario)



