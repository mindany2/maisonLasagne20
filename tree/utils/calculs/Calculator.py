from tree.utils.List import List
from random import randint
from tree.scenario.Scenario import MARKER
from tree.utils.Logger import Logger
import re

class Calculator:
    """
    Calculate the expressions
    """
    def __init__(self):
        self.variables = List()

    def add(self, var):
        try:
            self.variables.get(var.name)
            Logger.warn("The variable {} is already present".format(var.name))
        except (KeyError, ValueError):
            self.variables.add(var)

    def eval(self, expression, inst=None):
        string = str(expression)
        if string:
            # search for variables names
            for var in re.split("[\*,\-,\+,\/,\(,\),<,>,|, ]", string):
                if not(var):
                    continue
                try:
                    int(var)
                except ValueError:
                    try:
                        int(var, 16)
                    except ValueError:
                        if var not in ("False", "True", "not", "randint"):
                            # replace the var_name by it's value
                            string = string.replace(var,"self.get_value(\"{}\",expression, inst)".format(var))
            try:
                return eval(string)
            except SyntaxError as e:
                expression.raise_error(str(e))
                
        return 0

    def get_value(self, var_name, expression, inst):
        cutted_name = var_name.split(".")[0]
        try:
            return self.variables.get(cutted_name).get(inst, expression.get_getter(), var_name)
        except KeyError:
            expression.raise_error("Could not find the variable {}".format(var_name))

    def reset(self):
        # reset the inst list of all variables
        for var in self.variables:
            var.reset()


    def get(self, name):
        return self.variables.get(name)

    def get_list_variables(self):
        return self.variables

    def __str__(self):
        return str(self.variables)

