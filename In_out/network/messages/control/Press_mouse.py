from In_out.network.messages.Message import Message
from In_out.network.pc_control.Controller import Controller

class Press_mouse(Message):

    def __init__(self, x, y, clic_right = False, double_clic = False):
        self.x = x
        self.y = y
        self.clic_right = clic_right
        self.double_clic = double_clic

    def do(self):
        Controller().press_mouse(self.x, self.y, self.clic_right, self.double_clic)
