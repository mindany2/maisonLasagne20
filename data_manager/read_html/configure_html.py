from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.utils.file_manager import list_folders, list_files

from tree.utils.Color import Color

from web_app.buttons.Line_buttons import Line_buttons
from web_app.buttons.Button import Button

PATH = "data/environnements"

def config_html(getter):
    # go to each environnement and find every define html line
    # and store it in the getter

    get_lines(getter, PATH, "global")

    print(getter)

def get_lines(getter, path, env_name):
    for preset in list_files(path+"/presets"):
        get_line(getter, path+"/presets/"+preset, env_name,preset.split(".yaml")[0])

    for sub_env in list_folders(path):
        if sub_env != "presets":
            get_lines(getter, path+"/"+sub_env, env_name+"."+sub_env)

def get_line(getter, path, env_name, preset_name):
    file = File_yaml(getter, path)
    html = file.get("HTML")
    if html:
        name, colors = html.get_str("name", mandatory=True), html.get_str("colors")
        if colors:
            colors = [Color(color) for color in colors.split(",")]

        try:
            line = getter.get_line(name)
        except KeyError:
            line = Line_buttons(name, env_name, preset_name, colors)
            getter.add_line(line)
        html.get("buttons", method=get_buttons, args = line, mandatory=True)

def get_buttons(buttons, line):
    for button in Csv_reader(buttons.get_getter(), buttons):
        line.add_button(Button(button.get_str("name", mandatory=True)))





