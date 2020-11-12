from utils.communication.Message import Message
from In_out.communication.pc_control.Controlleur import Controlleur

class Press_key(Message):

    def __init__(self, key):
        self.key = key

    def do(self):
        Controlleur().press_key(self.key)
