from utils.spotify.Spotify import Spotify
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
        if self.wait_for_beat != 0:
            # we need to wait some beats
            numero = calculator.eval(self.wait_for_beat)
            Spotify.wait_for_beat(numero)
        sleep(calculator.eval(self.str_val)-time_spent)
