from tree.utils.List import List
from tree.scenario.Scenario import MARKER

class Scenario_manager:
    """
    Manage the scenario order
    """
    def __init__(self):
        # the scenario selecter :
        #   this is the choice of the environnement, only a principal button can change it's value
        #   if this scenario is OFF, the top secondary scenario in the stack is done
        #   if the stack is empty, just do the scenar OFF
        self.scenario_select = None
        # store in order secondaries scenarios
        self.stack = []

        self.current_scenar = None

    def initialize(self, scenar_init):
        self.scenario_select = scenar_init
        self.current_scenar = scenar_init
        self.current_scenar.set_state(True)

    def do_current_scenar(self):
        print(self.current_scenar.name)
        self.current_scenar.do()

    def do(self, scenar):
        # start the scenario
        self.current_scenar.set_state(False)
        self.current_scenar = scenar
        self.current_scenar.set_state(True)
        self.current_scenar.do()

    def do_scenar_principal(self, scenar):
        """
        This method is call to modifie the principal scenario of the environnement
        """
        if not(self.scenario_select):
            # manager not initialize
            # i could append with linked scenarios
            return 
        if scenar.get_marker() == MARKER.NONE:
            # none scenario are just invisible
            scenar.do()
            return
        elif scenar.get_marker() != MARKER.OFF:
            # if it is ON
            self.do(scenar)
        elif self.scenario_select.get_marker() == MARKER.OFF:
            # if we are already OFF, so just clear the list an shutdown 
            self.do(scenar)
            self.stack.clear()
        else: 
            if len(self.stack) == 0:
                self.do(scenar)
            else:
                # do the top of the stack if it is not empty
                self.do(self.top())
        self.scenario_select = scenar

    def do_scenar_secondary(self, scenar):
        """
        This method is call to modifie secondaries scenarios to and in the stack
        """
        if scenar.get_marker() == MARKER.NONE:
            # null scenario are just invisible
            scenar.do()
            return
        self.stack.append(scenar)
        if self.scenario_select.get_marker() == MARKER.OFF:
            self.do(scenar)

    def get_scenar_select(self):
        return self.scenario_select

    def get_current_scenar(self):
        return self.current_scenar

    def get_stack(self):
        return self.stack

    def reload_scenar_selected(self, scenario_select):
        self.scenario_select = scenario_select

    def reload_current_scenar(self, scenario):
        self.current_scenar = scenario
        self.current_scenar.do()

    def reset(self):
        self.stack.clear()
        self.current_scenar.set_state(True)
        self.current_scenar = None
        self.scenario_select = None

    def push(self, scenar):
        self.stack.append(scenar)

    def remove(self, scenar):
        """
        Call to remove a scenario for the stack
        """
        if scenar.get_marker() == MARKER.NONE:
            # none scenario are just invisible
            return
        try:
            self.stack.remove(scenar)
        except ValueError:
            pass
        if self.current_scenar is scenar: # is is the current_scenar
            # do the appropriate scenario
            if len(self.stack) == 0 or self.scenario_select.get_marker() != MARKER.OFF:
                self.do(self.scenario_select)
            else:
                self.do(self.top())

    def top(self):
        return self.stack[-1]

    def get_state(self):
        return self.current_scenar.get_marker() == MARKER.ON

    def get_principal_state(self):
        return self.scenario_select.get_marker() == MARKER.ON

    def get_marker(self):
        return self.current_scenar.get_marker()

    def __str__(self):
        string = "principal : {} {}\n".format(self.scenario_select.name, self.scenario_select.state())
        string += "current : {} {}\n".format(self.current_scenar.name, self.current_scenar.state())
        string += "stack : "+", ".join([ scenar.name for scenar in self.stack])
        return string


