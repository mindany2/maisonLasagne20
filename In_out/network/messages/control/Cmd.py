from In_out.network.messages.Message import Message
import os

class Cmd(Message):

    def __init__(self, command):
        self.command = command

    def do(self, getter):
        os.system(self.command)
