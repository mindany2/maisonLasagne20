from tree.utils.List import List

class Line_buttons:
    """
    Store a line of button like to a preset in the tree
    """

    def __init__(self, name, env_name, preset_name, colors):
        self.name = name
        self.colors = colors
        # path of all the preset link to this line
        self.env_name = env_name 
        self.preset_name = preset_name 
        self.buttons = List()
        self.style = None
        self.state = False

    def change_state(self, state):
        self.state = state

    def set_style(self, style):
        self.style = style

    def get_style(self):
        return self.style

    def add_button(self, button):
        self.buttons.add(button)

    def get_link(self):
        return "{}.{}".format(self.env_name, self.preset_name)

    def nb_buttons(self):
        return len(self.buttons)

    def get_buttons(self):
        return self.buttons

    def get_button(self, name):
        return self.buttons.get(name)

    def __str__(self):
        string = "- name : {}\n".format(self.name)
        string += "- env : {}\n".format(self.env_name)
        string += "- preset : {}\n".format(self.preset_name)
        string += "- state : {}\n".format(self.state)
        string += "- colors : {}\n".format(self.colors)
        string += "".join("|  {}\n".format(string) for string in str(self.buttons).split("\n"))
        return string
