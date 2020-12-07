from data_manager.utils.file_manager import list_files
from data_manager.utils.File_yaml import File_yaml
from data_manager.configure_instructions import get_instructions

from tree.Preset import Preset

from tree.scenario.Scenario import Scenario, MARKER


def get_presets(env, path):
    for preset_yaml in list_files(path):
        name = preset_yaml.split(".")[0]
        file = File_yaml("{}/{}".format(path, preset_yaml))
        preset = Preset(name)

        # Scenarios
        file.get("Scenarios", get_scenarios, args = [preset, env])

        env.add_preset(preset)

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



