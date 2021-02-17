from tree.utils.List import List
from tree.scenario.Scenario import MARKER
from threading import Lock
from tree.utils.Logger import Logger

class Scenario_manager:
    """
    Manage the scenario order
    """
    def __init__(self, name):
        # the scenario selecter :
        #   this is the choice of the environnement, only a principal button can change it's value
        #   if this scenario is OFF, the top secondary scenario in the stack is done
        #   if the stack is empty, just do the scenar OFF
        self.scenario_select = None
        # store in order secondaries scenarios
        self.stack = []

        self.name = name

        self.current_scenar = None

        self.mutex = Lock()

    def initialize(self, scenar_init):
        self.scenario_select = scenar_init
        self.current_scenar = scenar_init
        self.current_scenar.set_state(True)

    def do_current_scenar(self):
        Logger.info("Do scenario {}.{}".format(self.name, self.current_scenar.name))
        self.mutex.acquire()
        self.current_scenar.do()
        self.mutex.release()

    def do(self, scenar):
        # start the scenario
        if self.current_scenar is not scenar:
            self.current_scenar.set_state(False)
            self.current_scenar = scenar
            self.current_scenar.set_state(True)
            self.current_scenar.do()
            Logger.info("Do scenario {}.{}".format(self.name, self.current_scenar.name))

    def do_scenar_principal(self, scenar):
        """
        This method is call to modifie the principal scenario of the environnement
        """
        self.mutex.acquire()
        if not(self.scenario_select):
            # manager not initialize
            # i could append with linked scenarios
            self.mutex.release()
            return 
        if scenar.get_marker() == MARKER.NONE:
            # none scenario are just invisible
            scenar.do()
            self.mutex.release()
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
        self.mutex.release()

    def do_scenar_secondary(self, scenar):
        """
        This method is call to modifie secondaries scenarios to and in the stack
        """
        self.mutex.acquire()
        if scenar.get_marker() == MARKER.NONE:
            # null scenario are just invisible
            scenar.do()
            self.mutex.release()
            return
        self.stack.append(scenar)
        if self.scenario_select.get_marker() == MARKER.OFF:
            self.do(scenar)
        self.mutex.release()

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
        self.mutex.acquire()
        if scenar.get_marker() == MARKER.NONE:
            # none scenario are just invisible
            self.mutex.release()
            return
        try:
            self.stack.remove(scenar)
        except ValueError:
            pass
        if self.current_scenar is scenar: # it is the current_scenar
            # do the appropriate scenario
            if len(self.stack) == 0 or self.scenario_select.get_marker() != MARKER.OFF:
                self.do(self.scenario_select)
            else:
                self.do(self.top())
        self.mutex.release()

    def top(self):
        return self.stack[-1]

    def get_state(self):
        return self.current_scenar.get_marker() == MARKER.ON

    def get_principal_state(self):
        return self.scenario_select.get_marker() == MARKER.ON

    def get_marker(self):
        return self.current_scenar.get_marker()

    def __str__(self):
        string = "principal : {}\n".format(self.scenario_select.name)
        string += "current : {}\n".format(self.current_scenar.name)
        string += "stack : "+", ".join([ scenar.name for scenar in self.stack])
        return string


