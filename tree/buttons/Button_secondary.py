from tree.buttons.Button import Button
from tree.scenario.Scenario import MARKER

class Button_secondary(Button):
    """
    Button that is not directly link with the env that have the scenario
    so used the stack of the manager
    """
    def __init__(self, name, manager, scenar):
        Button.__init__(self, name, manager)
        self.scenar = scenar

    def state(self):
        return self.scenar.state()

    def press(self, state = True):
        if state:
            # do the scenario
            self.manager.do_scenar_secondaire(self.scenar)
        else:
            # remove the scenario
            self.manager.remove(self.scenar)


