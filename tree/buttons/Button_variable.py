from tree.buttons.Button import Button
from tree.utils.Logger import Logger

class Button_variable(Button):
    """
    Button that just set a variable
    """
    def __init__(self, name, variable):
        Button.__init__(self, name)
        self.variable = variable

    def state(self):
        return self.variable.get()

    def press(self, val = None):
        if val:
            Logger.info(f"Set {self.variable.get_name()} to {val}")
            self.variable.set(val)

    def __eq__(self, other):
        if isinstance(other, Button_variable):
            return super().__eq__(other)\
                    and self.variable == other.variable
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : variable\n")
        string += "".join("- variable : {}\n".format(self.variable.name))
        return string



