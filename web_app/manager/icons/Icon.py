from enum import Enum

class TYPE_ICON(Enum):
    button = "image"
    text = 0

class Icon:
    """
    This is an icon on the html page
    """
    def __init__(self, name, index = 100, lenght = 1):
        self.name = name
        self.index = index
        self.lenght = lenght
        self.style = None
        self.state = True

    def get_index(self):
        return self.index

    def get_type(self):
        return None

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_lenght(self):
        return self.lenght

    def get_style(self):
        return self.style

    def pack(self, i=0, j=0):
        raise(AttributeError("Need to setup the style in subclass"))

    def __str__(self):
        return "{} : lenght={}".format(self.name, self.lenght)
