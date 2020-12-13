from tree.utils.List import List
from tree.utils.Dico import Dico
from tree.scenario.Scenario import MARKER
from tree.scenario.Scenario_manager import Scenario_manager

class Preset:
    """
    Store a list of scenario, and a list of insterrupt to run them
    """
    def __init__(self, name):
        self.name = name
        self.list_scenario = List()
        self.buttons = List()
        self.manager = Scenario_manager()
        self.state = False

    def add_button(self, button):
        self.buttons.add(button)

    def get_button(self, name_inter):
        return self.buttons.get(name_inter)

    def press_inter(self, name_inter, state):
        try:
            bt = self.get_button(name_inter)
            if bt != None:
                bt.press(state)
        except:
            pass

    def change_state(self, state):
        self.state = state

    def add_scenar(self, scenar):
        self.list_scenario.add(scenar)

    def get_scenar(self, name):
        return self.list_scenario.get(name)

    def get_manager(self):
        if self.manager:
            return self.manager
        raise(ValueError("Need to setup a OFF scenario in the preset "+self.name)) 

    def get_marker(self):
        return self.get_manager().get_marker()

    def reset(self):
        self.get_manager().reset()

    def initialize(self, marker):
        # get the first OFF scenario for the manager
        scenar_select = None
        for scenar in self.list_scenario:
            if not(scenar_select) and scenar.get_marker() == marker:
                scenar_select = scenar
        if scenar_select:
            # we have the same marker
            self.manager.initialize(scenar_select)
        elif marker != MARKER.OFF:
            # setup the OFF by default
            self.initialize(MARKER.OFF)
        else:
            raise(ValueError("Need to setup a OFF scenario in the preset {}".format(self.name)))

        # initialize all the scenarios
        for scenar in self.list_scenario:
            scenar.initialize()

    def reload(self, other):
        if isinstance(other, Preset):
            self.state = other.state

    def get_buttons(self):
        return self.buttons

    def get_list_scenars(self):
        return self.list_scenario

    def __eq__(self, other):
        if isinstance(other, Preset):
            return self.name == other.name\
                    and self.list_scenario == other.list_scenario\
                    and self.buttons == other.buttons
        return False

    def __str__(self):
        string = self.name + "\n"
        string += "".join("- Scenarios\n")
        string += "".join(["  |{}\n".format(string) for string in str(self.list_scenario).split("\n")])
        string += "".join("- Buttons\n")
        string += "".join(["  |{}\n".format(string) for string in str(self.buttons).split("\n")])
        return string
