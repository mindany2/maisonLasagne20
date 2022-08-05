from data_manager.utils.file_manager import list_files
from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.read_tree.configure_instructions import get_instructions

from tree.Preset import Preset

from tree.scenario.Scenario import Scenario, MARKER
from tree.buttons.Button_principal import Button_principal
from tree.buttons.Button_secondary import Button_secondary
from tree.buttons.Button_choice import Button_choice
from tree.buttons.Button_variable import Button_variable
from tree.buttons.Button_tempo import Button_tempo
import re


def get_presets(getter, env, path):
    for preset_yaml in list_files(path):
        name = preset_yaml.split(".")[0]
        file = File_yaml(getter, "{}/{}".format(path, preset_yaml))
        preset = Preset(name, env.name)

        # Scenarios
        file.get("Scenarios", get_scenarios, args = [preset, env])

        # Interrupts Button
        interrupts = file.get("Interrupts")
        if interrupts:
            interrupts.get("buttons", get_inter_buttons, args = preset, mandatory = True)

        # HTML Button
        html = file.get("HTML")
        if html:
            get_html_buttons(html, preset, env)

        env.add_preset(preset)

def get_html_buttons(buttons, preset, env):
    for button in buttons:
        action, name = button.get("action", mandatory=True), button.get_str("name", mandatory=True)
        type_action = action.get("type")
        if str(type_action) == "button":
            type_bt, scenars = action.get("button", mandatory=True), action.get("scenarios", mandatory=True)
            preset.add_button(get_bt(name, preset, type_bt, scenars))
        elif str(type_action) == "variable":
            var_name = action.get_str("variable", mandatory=True)
            try:
                variable = env.get_var(var_name)
            except NameError as e:
                var_name.raise_error(e)
            preset.add_button(Button_variable(name, variable))
        else:
            type_action.raise_error("Type action is not correct")

        # check if the image is static, if not, it could be a spotify picture
        image = button.get("background_image")
        if image and not(re.search(r"\.png|\.jpg|\.jpeg", str(image))):
            if re.search("spotify.",str(image)):
                image.get_spotify().add_state(name, list(image.split("."))[1])
            else:
                image.raise_error("Invalid format for the image need [png,jpg,jpeg]")



def get_inter_buttons(buttons, preset):
    getter = buttons.get_getter()
    for inter in Csv_reader(getter, buttons):
        name, type_bt, scenars = inter.get_str("name", mandatory=True), inter.get("type", mandatory=True), inter.get("scenarios", mandatory=True)
        preset.add_button(get_bt(name, preset, type_bt, scenars))

def get_bt(name, preset, type_bt, scenars):
        try:
            manager = preset.get_manager()
        except ValueError as e:
            type_bt.raise_error(str(e))
        list_scenar = []
        for scenar in scenars.split(","):
            try:
                list_scenar.append(preset.get_scenar(str(scenar)))
            except KeyError:
                scenar.raise_error("Could not found scenario {} in preset {}".format(str(scenar), preset.name))

        if str(type_bt) == "principal":
            scenar2 = None
            if len(list_scenar) > 1:
                scenar2 = list_scenar[1]
            return Button_principal(name, manager, list_scenar[0], scenar2)
        elif str(type_bt) == "secondary":
            return Button_secondary(name, manager, list_scenar[0])
        elif str(type_bt) == "choice":
            return Button_choice(name, manager, list_scenar)
        elif str(type_bt).count("tempo"):
            type_, tempo = type_bt.split(",",2)
            return Button_tempo(name, manager, list_scenar[0], list_scenar[1], int(tempo))

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



