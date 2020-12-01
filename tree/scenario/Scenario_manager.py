from tree.utils.List import List
from tree.scenario.Scenario import MARKER

class Scenario_manager:
    """
    Manage the scenario order
    """
    def __init__(self, scenar_init):
        # the scenario selecter :
        #   this is the choice of the environnement, only a principal button can change it's value
        #   if this scenario is OFF, the top secondary scenario in the stack is done
        #   if the stack is empty, just do the scenar OFF
        self.scenario_select = scenar_init
        # store in order secondaries scenarios
        self.stack = List()

        self.current_scenar = scenar_init
        # just to the init scenario
        self.do(scenar_init)

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
        if scenar.get_marker() == MARKER.NULL:
            # null scenario are just invisible
            scenar.do()
            return
        elif scenar.get_marker() != MARKER.OFF:
            # if it is ON
            self.do(scenar)
        elif self.scenario_select.get_marker() == MARKER.OFF:
            # if we are already OFF, so just clear the list an shutdown 
            self.do(scenar)
            self.stack.clear()
        else: # do the top of the stack if it is not empty
            if not(self.stack.is_empty()):
                self.do(self.top())
        self.scenario_select = scenar

    def do_scenar_secondaire(self, scenar):
        """
        This method is call to modifie secondaries scenarios to and in the stack
        """
        if scenar.get_marker() == MARKER.NULL:
            # null scenario are just invisible
            scenar.do()
            return
        self.stack.add(scenar)
        if self.scenario_select.get_marker() == MARKER.OFF:
            self.do(scenar)

    def get_scenar_select(self):
        return self.scenario_select

    def get_current_scenar(self):
        return self.current_scenar

    def push(self, scenar):
        self.stack.add(scenar)

    def remove(self, scenar):
        """
        Call to remove a scenario for the stack
        """
        if scenar.get_marker() == MARKER.NULL:
            # null scenario are just invisible
            return
        self.stack.remove(scenar)
        if self.current_scenar == scenar: # is is the current_scenar
            # do the appropriate scenario
            if self.stack.is_empty() or self.scenario_select.get_marker() != MARKER.OFF:
                self.do(self.scenario_select)
            else:
                self.do(self.top())

    def top(self):
        return self.stack.last()

    def get_marker(self):
        return self.scenario_select.get_marker()


