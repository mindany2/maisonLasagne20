from tree.buttons.Button import Button

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

    def __eq__(self, other):
        if isinstance(other, Button_secondary):
            return super().__eq__(other)\
                    and self.scenar == other.scenar
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : secondary\n")
        string += "".join("- scenar : {}\n".format(self.scenar.name))
        return string



