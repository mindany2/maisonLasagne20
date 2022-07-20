from In_out.network.messages.Message import Message
from In_out.network.pc_control.Controller import Controller

class Press_key(Message):

    def __init__(self, keys):
        self.keys = keys

    def do(self, getter):
        Controller().press_key(self.keys)
