from pynput import mouse, keyboard
from utils.Logger import Logger

class Listener:
    """
    Permet d'ecouter toutes les entrées clavier et click sourie
    """
    def __init__(self):
        self.mouse_listener = mouse.Listener(on_click = self.click)
        self.mouse_listener.start()
        
        self.keyboard_listener = keyboard.Listener(on_press = self.key)
        self.keyboard_listener.start()

    def click(self, x, y, button, pressed):
        if pressed:
            Logger.info("{} : {}".format(button, (x,y)))

    def key(self, key):
         Logger.info(key)



