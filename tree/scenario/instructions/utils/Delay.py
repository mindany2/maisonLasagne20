from time import sleep

class Delay:
    """
    An int value that is store to wait a certain amount of time
    Or wait for a new beat
    """
    def __init__(self, manager, calculator, val, wait_for_beat = 0):
        self.val = val
        self.wait_for_beat = wait_for_beat
        self.manager = manager
        self.calculator = calculator

    def initialize(self):
        self.calculator.eval(self.val)

    def wait(self, time_spent = 0):
        if self.calculator.eval(self.wait_for_beat) != 0:
            # we need to wait some beats
            number = self.calculator.eval(self.wait_for_beat)
            self.manager.get_spotify().wait_for_beat(number)
        tps = self.calculator.eval(self.val)-time_spent
        if tps > 0:
            sleep(tps)

    def __str__(self):
        return str(self.val)
