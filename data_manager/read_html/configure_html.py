from data_manager.utils.File_yaml import File_yaml
from data_manager.utils.Csv_reader import Csv_reader
from data_manager.utils.file_manager import list_folders, list_files
from web_app.manager.Page import Page
from web_app.manager.Section import Section
from web_app.manager.icons.Icon_button import Icon_button
from web_app.manager.icons.Icon_redirect import Icon_redirect

from tree.utils.Color import Color

PATH = "/data"

def config_html(manager, path):
    # go to each environnement and find every define html line
    # and store it in the manager

    get_pages(manager, path+PATH)

    parkour_presets(manager, path+ PATH + "/environnements", "global")

    get_button_mode(manager, path+PATH)

    print(manager)

def get_button_mode(manager, path):
    file = File_yaml(manager, path+"/config.yaml")
    for mode in file.get("MODES", mandatory=True):
        html, name = mode.get("html"), mode.get_str("name", mandatory=True)
        if html:
            get_icons(manager, html, "mode."+name)

def get_pages(manager, path):
    for page in list_files(path+"/pages"):
        get_page(manager, path+"/pages/"+page, page.split(".yaml")[0])

def get_page(manager, path, name):
    """
    Create page
    """
    file = File_yaml(manager, path)
    config = file.get("Config")
    if config:
        background_color, background_image = config.get_str("background_color"), config.get_str("background_image")
        page = Page(name, background_image=background_image, background_color=background_color)
    else:
        page = Page(name)
    manager.add_page(page)
        
    # get sections
    for section in file.get("Sections", mandatory=True):
        page.add_section(get_section(section, page))

    # get static icons
    icons = file.get("Static_icons")
    if icons:
        for icon in icons:
            section, name = icon.get_str("section", mandatory=True), icon.get_str("name", mandatory=True)
            page.get_section(section).add_icon(get_icon(name, icon))

def get_section(section, page):
    name, title = section.get_str("name", mandatory=True), section.get_str("title")
    lenght, index = section.get_int("lenght"), section.get_int("index")
    background_color, text_color = section.get_str("background_color"), section.get_str("text_color")
    return Section(name, index = index, title = title, lenght = lenght,
            background_color = background_color, text_color= text_color)


def parkour_presets(manager, path, env_name):
    for preset in list_files(path+"/presets"):
        html = File_yaml(manager, path+"/presets/"+preset).get("HTML")
        if html:
            get_icons(manager, html, env_name)

    for sub_env in list_folders(path):
        if sub_env != "presets":
            parkour_presets(manager, path+"/"+sub_env, env_name+"."+sub_env)

def get_icons(manager, html, env_name):
    for icon in html:
        page, section, name = icon.get("name").split(".", number=3)
        manager.get_page(str(page)).get_section(str(section)).add_icon(get_icon(str(name), icon, env=env_name))

def get_icon(name, icon, env=None):
    """
    Create an icon and add it to the right section
    """
    manager = icon.get_getter()

    type_icon, lenght, index = icon.get("type", mandatory=True), icon.get_int("lenght"), icon.get_int("index")
    if str(type_icon) == "button":
        image, color_on = icon.get_str("background_image", mandatory=True), icon.get_str("active_color", mandatory=True)
        color_off = icon.get_str("inactive_color")
        if str(env) == None:
            env.raise_error("A button need to have a link to an environnement")
        return Icon_button(name, str(env), image, color_on, color_off, index = index, lenght=lenght)

    elif str(type_icon) == "redirection":
        image, background_color = icon.get_str("background_image", mandatory=True), icon.get_str("background_color")
        link = icon.get_str("link", mandatory=True)
        return Icon_redirect(name, image, link, background_color= background_color, index = index, lenght=lenght)

    type_icon.raise_error("Type icon unknown")








