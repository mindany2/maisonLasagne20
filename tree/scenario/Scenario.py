from tree.scenario.Instructions_list import Instructions_list
from threading import Thread
from enum import Enum
from tree.utils.Logger import Logger

class MARKER(Enum):
    """
    There are different type of scenario
    """
    OFF = 0
    ON = 1
    DECO = 2
    NULL = 3

class Scenario:
    """
    A Scenario with a list of instructions
    """
    def __init__(self, name, marker,calculator, loop = False):
        self.name = name
        self.list_inst = Instructions_list(loop, calculator)
        self.marker = marker

    def add_inst(self, inst):
        self.list_inst.add(inst)

    def get_marker(self):
        return self.marker

    def state(self):
        return self.list_inst.state

    def reload(self, other):
        if isinstance(other, Scenario):
            self.set_state(other.state())

    def set_state(self, state):
        self.list_inst.set_state(state)

    def do(self, join = False):
        Logger.info("On fait le scénario "+self.name)
        proc = Thread(target=self.list_inst.do)
        proc.start()
        if join:
            proc.join()

    def __eq__(self, obj):
        if isinstance(obj, Scenario):
            # si les list_inst finissent pareil
            return self.list_inst == obj.list_inst
        return False

    def initialize(self):
        self.list_inst.initialize()

    def __str__(self):
        string = self.name + "\n"
        string += "".join("- Marker : {}\n".format(self.marker))
        string += "".join("- List Instructions :\n")
        string += "".join(["  {}\n".format(string) for string in str(self.list_inst).split("\n")])
        return string
