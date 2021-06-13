from tree.utils.calculs.Variable import Variable
import re

class Variable_env(Variable):
    """
    Allow to find a variable in another env
    """
    def __init__(self, tree):
        self.tree = tree
        Variable.__init__(self, "env", 0)

    def get(self, inst, variable_name):
        match = re.match(r'env.(?P<env>([\w\.]*))\.(?P<var>([^\,]*))', variable_name)
        if match:
            path_env, name_var = match.group("env"), match.group("var")
        else:
            raise(KeyError("Could not found a variable like : env.env1.subenv.variable1"))
        try:
            env = self.tree.get_env(path_env)
        except KeyError:
            raise(KeyError(f"The env {path_env} does not exist"))
        try:
            var = env.get_var(name_var)
            return var.get(inst)
        except KeyError:
            # it can be a state variable
            if name_var.count("state"):
                return env.state()
            elif name_var.count("is_on"):
                return env.is_on()
            raise(KeyError("The variable {} in the environnement {} doesn't existe".format(variable_name, path_env)))

    def reload(self, other):
        pass

    def set(self, val):
        raise(ReferenceError("Cannot set an this variable"))
        
