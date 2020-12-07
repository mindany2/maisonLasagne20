from enum import Enum
from time import sleep,time
from In_out.utils.ST_nucleo import STATE_TRIAK

class Triak:
    """
    This is a triak connected through a ST_nucleo card
    """
    def __init__(self, number_board, number_triak, stnucleo):
        self.number_board = number_board
        self.number_triak = number_triak
        self.value = 99999
        self.stnucleo = stnucleo

    def set(self, value, state=STATE_TRIAK.dimmer):
        if self.value != value:
            self.stnucleo.set_triak(self.number_board, self.number_triak, value, state)
            self.value = value

    def __str__(self):
        return "{}({})".format(self.number_triak,self.number_board)
