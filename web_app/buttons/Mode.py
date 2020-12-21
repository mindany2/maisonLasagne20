
class Mode:
    """
    Setup a page with a color, css..
    """
    def __init__(self, name, color="white", text_color="black"):
        self.name = name
        self.color = color
        self.text_color = text_color
        self.state = False

    def change_state(self, state):
        self.state = state


