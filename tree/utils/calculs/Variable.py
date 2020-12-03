
class Variable:
    """
    Store a value
    """
    def __init__(self, name, val):
        self.name = name
        self.val = val

    def get(self, args = None):
        return self.val

    def set(self, val):
        self.val = val
        
    def __int__(self):
        return self.get()

    def __add__(self, integer):
        return int(self)+integer
