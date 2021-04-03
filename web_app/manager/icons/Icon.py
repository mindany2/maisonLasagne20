from enum import Enum
from tree.utils.Logger import Logger
import re

class TYPE_ICON(Enum):
    button = "image"
    link = 2
    text = 0
    slider = 3

class Icon:
    """
    This is an icon on the html page
    """
    def __init__(self, name, env=None, index = None, lenght = None, text=None):
        self.name = name
        self.index = 100 if index is None else index
        self.lenght = 1 if lenght is None else lenght
        self.text = "" if text is None else text
        self.style = None
        self.state = True
        self.value = 0
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
        print(self)

    def change_infos(self, infos):
        self.value = infos["value"]

    def get_lenght(self):
        return self.lenght

    def get_text(self):
        return self.text

    def get_style(self):
        return self.style

    def pack(self, i=0, j=0):
        raise(AttributeError("Need to setup the style in subclass"))

    def __str__(self):
        return "{} : lenght={}, state={}, value={}".format(self.name, self.lenght, self.state, self.value)
