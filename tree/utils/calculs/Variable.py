
class Variable:
    """
    Store a value
    """
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def get(self, getter = None, arg = None):
        return self.val

    def reload(self, other):
        if isinstance(other, Variable):
            self.val = other.val

    def set(self, val):
        self.val = val
        
    def __int__(self):
        return self.get()

    def __add__(self, integer):
        return int(self)+integer

    def __str__(self):
        return "{} = {}\n".format(self.name, self.val)
