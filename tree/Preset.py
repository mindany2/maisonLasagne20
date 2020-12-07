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
        self.inter_to_buttons = Dico()

        self.manager = None
        self.state = False

    def add_link_inter(self, name_inter, button):
        self.inter_to_buttons.add(name_inter, button)

    def get_button(self, name_inter):
        return self.inter_to_buttons.get(name_inter)

    def press_inter(self, name_inter, state):
        bt = self.get_button(name_inter)
        if bt != None:
            bt.press(state)

    def change_state(self, state):
        self.state = state

    def add_scenar(self, scenar):
        self.list_scenario.add(scenar)
        # TODO setup this in the initialisation like inst button
        # initialise the manager with the first scenario OFF found
        # /!\ Need to have obligatory a scenario OFF in the preset
        """
        if not(self.manager) and scenar.get_marker() == MARKER.OFF:
            self.manager = Scenario_manager(scenar)
        """

    def get_scenar(self, name):
        return self.list_scenario.get(name)

    def get_manager(self):
        if self.manager:
            return self.manager
        raise(ValueError("Need to setup a OFF scenario in the preset "+self.name)) 

    def get_marker(self):
        return self.get_manager().get_marker()

    def __str__(self):
        string = self.name + "\n"
        string += "".join("- Scenarios\n")
        string += "".join(["  |{}\n".format(string) for string in str(self.list_scenario).split("\n")])
        string += "".join("- Buttons\n")
        string += "".join(["  |{}\n".format(string) for string in str(self.inter_to_buttons).split("\n")])
        return string
