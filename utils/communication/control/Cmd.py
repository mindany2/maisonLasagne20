from utils.communication.Message import Message
import os

class Cmd(Message):

    def __init__(self, command):
        self.command = command

    def do(self):
        os.system(self.command)
