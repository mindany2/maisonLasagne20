from tree.utils.List import List
from random import randint
from tree.scenario.Scenario import MARKER
from tree.utils.calculs.Variable_env import Variable_env
from tree.utils.calculs.Variable_spotify import Variable_spotify
import re

class Calculator:
    """
    Calculate the expressions
    """
    def __init__(self, tree):
        self.variables = List()
        # just add the common variables
        self.variables.add(Variable_spotify())
        self.variables.add(Variable_env(tre))

    def add(self, var):
        self.variables.add(var)

    def int(self, string):
        if string != "":
            # search for variables names
            for var in re.split("[0-9,\*,\-,\+,\/,\(,\)]", string):
                if var:
                    # replace the var_name by it's value
                    string = string.replace(var,self.get_value(var))
            return eval(string)
        return 0

    def get_value(self, var_name):
        cutted_name = var_name.split(".")
        return self.variables.get(cutted_name).get(var_name)

    def eval(self, string):
        try:
            return int(string)
        except:
            return self.int(string)

    def get(self, name):
        return self.variables.get(name)
