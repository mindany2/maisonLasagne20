from tree.utils.Dico import Dico
from threading import Thread

class Variable:
    """
    Store a value
    """
    def __init__(self, name, val):
        self.name = name
        self.val = val
        self.list_inst = Dico()

    def get(self, inst, getter = None, arg = None):
        self.add_inst(inst)
        return self.val

    def add_inst(self, inst):
        self.list_inst.add(inst.get_id(), inst)

    def reload(self, other):
        if isinstance(other, Variable):
            self.val = other.val

    def set(self, val, duration):
        self.val = val
        for inst in self.list_inst:
            if inst.current:
                # do inst inst if it is currently running
                print(inst)
                Thread(target=inst.reload, args=[duration]).start()
        
    def __int__(self):
        return self.val

    def __add__(self, integer):
        return int(self)+integer

    def __str__(self):
        return "{} = {}\n".format(self.name, self.val)
