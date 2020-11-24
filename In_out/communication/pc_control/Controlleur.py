
try:
    from pynput.keyboard import Key
    from pynput.keyboard import Controller as Key_controller
    from pynput.mouse import Button
    from pynput.mouse import Controller as Mouse_controller
except:
    pass

from utils.Logger import Logger

class Controlleur:
    """
    Permet de controller le clavier et la sourie
    """
    def __init__(self):
        self.keyboard = Key_controller()
        self.mouse = Mouse_controller()

    def press_key(self, key):
        touche = key
        try:
            touche = Key[key]
        except:
            Logger.error("Wrong press_key demand : "+key)
        self.keyboard.press(touche)
        self.keyboard.release(touche)

    def set_mouse(self, x, y):
        self.mouse.position = (x,y)

    def press_mouse(self,x = None, y = None, clic_right = False, double_clic = False):
        if x and y:
            self.set_mouse(x,y)
        if clic_right:
            self.mouse.click(Button.right, 1+int(double_clic))
        else:
            self.mouse.click(Button.left, 1+int(double_clic))


