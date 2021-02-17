from tree.utils.Dico import Dico
from threading import Thread
from tree.utils.Logger import Logger

class Variable:
    """
    Store a value
    """
    def __init__(self, name, val):
        self.name = name
        self.val = val
        self.list_inst = Dico()

    def get(self, inst=None, getter = None, arg = None):
        if inst:
            self.add_inst(inst)
        return self.val

    def add_inst(self, inst):
        self.list_inst.add(inst.get_id(), inst)

    def reset(self):
        self.list_inst = Dico()

    def reload(self, other):
        if isinstance(other, Variable):
            self.val = other.val

    def set(self, val, duration=0):
        self.val = val
        for inst in self.list_inst:
            if inst.current:
                # do inst inst if it is currently running
                try:
                    proc = Thread(target=inst.reload, args=[duration])
                    proc.name = "Reload inst with variable {} : {}".format(self.name, str(inst))
                    proc.start()
                except Exception as e:
                    Logger.error(e)
        
    def __int__(self):
        return self.val

    def __add__(self, integer):
        return int(self)+integer

    def __str__(self):
        return "{} = {}\n".format(self.name, self.val)
