from enum import Enum
from tree.utils.Logger import Logger
import re

class TYPE_ICON(Enum):
    button = "image"
    text = 0

class Icon:
    """
    This is an icon on the html page
    """
    def __init__(self, name, env=None, index = None, lenght = None):
        self.name = name
        self.index = 100 if index is None else index
        self.lenght = 1 if lenght is None else lenght
        self.style = None
        self.state = True
        # some icon can be selected (like button)
        self.selected = False
        # the link to the env in the tree
        self.env = env

    def get_index(self):
        return self.index

    def get_type(self):
        return None

    def get_state(self):
        return self.state

    def change_state(self, state):
        self.state = state

    def change_selected(self, selected):
        self.selected = selected

    def get_lenght(self):
        return self.lenght

    def get_style(self):
        return self.style

    def pack(self, i=0, j=0):
        raise(AttributeError("Need to setup the style in subclass"))

    def __str__(self):
        return "{} : lenght={}".format(self.name, self.lenght)
