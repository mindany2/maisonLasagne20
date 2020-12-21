from pynput import mouse, keyboard

class Listener:
    """
    Allow to listen the key pressed
    """
    def __init__(self):
        self.mouse_listener = mouse.Listener(on_click = self.click)
        self.mouse_listener.start()
        
        self.keyboard_listener = keyboard.Listener(on_press = self.key)
        self.keyboard_listener.start()

    def click(self, x, y, button, pressed):
        if pressed:
            # TODO 
            print("{} : {}".format(button, (x,y)))

    def key(self, key):
         print(key)



