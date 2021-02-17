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
        self.duration = duration
        self.synchro = synchro
        self.calculator = calculator
        self.current = False
        self.id = uuid.uuid1()
        self.mutex_reload = Lock()
        self.mutex_current = Lock()

    def get_id(self):
        return self.id

    def run(self, time_spent = 0):
        if not(self.mutex_reload.locked()):
            self.current = True
        self.duration=self.eval(self.duration)
        if self.delay:
            self.delay.wait(time_spent)
        # next in sub-classes

    def reload(self, duration):
        # reload the inst without any delay or duration
        self.mutex_reload.acquire()
        save_vals = [self.delay, self.duration]
        self.delay, self.duration = None, duration
        self.run(Barrier(1))
        self.delay, self.duration = save_vals
        self.mutex_reload.release()

    def wait_precedent(self):
        if self.delay:
            return self.delay.wait_precedent
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
        return True

    def __str__(self):
        string = "- Duration : {}\n".format(self.duration)
        string += "".join("- Delay : {}\n".format(self.delay))
        return string
