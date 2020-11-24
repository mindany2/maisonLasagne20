from utils.communication.Message import Message
from In_out.communication.pc_control.Controlleur import Controlleur

class Press_mouse(Message):

    def __init__(self, x, y, clic_right = False, double_clic = False):
        self.x = x
        self.y = y
        self.clic_right = clic_right
        self.double_clic = double_clic

    def do(self):
        Controlleur().press_mouse(self.x, self.y, self.clic_right, self.double_clic)
