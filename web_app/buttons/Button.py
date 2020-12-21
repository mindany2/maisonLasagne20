
class Button:
    """
    A complete html button
    """
    def __init__(self, name):
        self.name = name
        self.style_on, self.style_off = None, None
        self.state = False

    def change_state(self, state):
        self.state = state

    def set_styles(self, style_on, style_off):
        self.style_on, self.style_off = style_on, style_off

    def get_style(self):
        return [self.style_off, self.style_on][self.state]

    def __str__(self):
        return "{} : {}".format(self.name, self.state)


