from enum import Enum
from time import sleep
from threading import Thread, Barrier, Lock
import uuid

class STATE(Enum):
    CONTINUE = 0
    WAIT = 1

class Instruction:
    """
    This class is the parent class of all instructions
    """
    def __init__(self, calculator, duration, delay, synchro):
        self.delay = delay
        self.fixed_duration = duration #duration define in the data
        self.duration = duration
        self.synchro = synchro
        self.calculator = calculator
        self.current = False
        self.id = uuid.uuid1()
        self.in_reload = []
        self.mutex_current = Lock()

    def get_id(self):
        return self.id

    def run(self, time_spent = 0):
        if not(self.in_reload):
            self.current = True
            self.duration=self.eval(self.fixed_duration)
            if self.delay:
                self.delay.wait(time_spent)
        else:
            self.duration = self.in_reload.pop()
        # next in sub-classes

    def reload(self, duration):
        # reload the inst without any delay or duration
        self.in_reload.append(duration)
        self.run()

    def wait_precedent(self):
        if self.delay:
            return self.delay.get_wait_precedent()
        return False

    def finish(self):
        self.current = False

    def eval(self, string):
        return self.calculator.eval(string, self)

    def initialize(self):
        # verify if the expressions given can be resolved
        self.delay.initialize()
        self.eval(self.duration)

    def __eq__(self, other):
        if isinstance(other, Instruction):
            return self.delay == other.delay\
                    and self.calculator == other.calculator\
                    and self.fixed_duration == other.fixed_duration\
                    and self.synchro == other.synchro
        return False

    def __str__(self):
        string = "- Duration : {}\n".format(self.duration)
        string += "".join("- Delay : {}\n".format(self.delay))
        return string
