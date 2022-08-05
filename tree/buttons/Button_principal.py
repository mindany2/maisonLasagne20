from tree.buttons.Button import Button

class Button_principal(Button):
    """
    Button that use the principal scenario of the environnement
    if there are not a scenar_off, it juste do scenar_on
    """
    def __init__(self, name, manager, scenar_on, scenar_off = None):
        Button.__init__(self, name, manager)
        self.scenar_on = scenar_on
        self.scenar_off = scenar_off

    def state(self):
        return self.manager.get_state()

    def press(self, state = None):
        if self.scenar_off:
            # if there are 2 scenarios
            if state == None:
                state = not(self.state())

            if state:
                self.manager.do_scenar_principal(self.scenar_on)
            else:
                self.manager.do_scenar_principal(self.scenar_off)
        else:
            # simple button, juste do the scenar_on
            self.manager.do_scenar_principal(self.scenar_on)

    def __eq__(self, other):
        if isinstance(other, Button_principal):
            return super().__eq__(other)\
                    and self.scenar_on == other.scenar_on\
                    and self.scenar_off == other.scenar_off
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : principal\n")
        string += "".join("- ON : {}\n".format(self.scenar_on.name))
        if self.scenar_off:
            string += "".join("- OFF : {}\n".format(self.scenar_off.name))
        return string



