import time

class Delay:
    """
    An int value that is store to wait a certain amount of time
    Or wait for a new beat
    """
    def __init__(self, manager, calculator, val, wait_for_beat = 0, wait_precedent = False):
        self.val = val
        self.wait_precedent = wait_precedent
        self.wait_for_beat = wait_for_beat
        self.manager = manager
        self.calculator = calculator

    def get_wait_precedent(self):
        return self.wait_precedent

    def initialize(self):
        self.calculator.eval(self.val)

    def wait(self, time_spent = 0):
        if self.calculator.eval(self.wait_for_beat) != 0:
            # we need to wait some beats
            number = self.calculator.eval(self.wait_for_beat)
            self.manager.get_spotify().wait_for_beat(number)
        tps = self.calculator.eval(self.val)-time_spent
        if tps > 0:
            time.sleep(tps)

    def __str__(self):
        return str(self.val)
