from In_out.Peripheric_manager import Peripheric_manager
from time import sleep

class Delay:
    """
    An int value that is store to wait a certain amount of time
    Or wait for a new beat
    """
    def __init__(self, str_val, wait_for_beat = 0):
        self.str_val = str_val
        self.wait_for_beat = wait_for_beat

    def wait(self, calculator, time_spent = 0):
        if calculator.eval(self.wait_for_beat) != 0:
            # we need to wait some beats
            number = calculator.eval(self.wait_for_beat)
            Peripheric_manager.get_spotify().wait_for_beat(number)
        sleep(calculator.eval(self.str_val)-time_spent)

    def __str__(self):
        return self.str_val
