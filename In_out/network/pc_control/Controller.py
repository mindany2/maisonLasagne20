from time import sleep

try:
    from pynput.keyboard import Key
    from pynput.keyboard import Controller as Key_controller
    from pynput.mouse import Button
    from pynput.mouse import Controller as Mouse_controller
except ModuleNotFoundError as err:
    # need to install the module
    raise(err)
except:
    # the rpis haven't any graphicals setup, so just pass
    pass

class Controller:
    """
    Allows to control the mouse and the keyboard
    """
    def __init__(self):
        self.keyboard = Key_controller()
        self.mouse = Mouse_controller()

    def press_key(self, keys, time_kept = 0):
        # convert need keys
        list_keys = []
        for key in keys:
            try:
                list_keys.append(Key[key])
            except ValueError:
                list_keys.append(key)
        for key in list_keys:
            self.keyboard.press(keys)
        sleep(time_kept)
        for key in list_keys:
            self.keyboard.release(keys)

    def set_mouse(self, x, y):
        self.mouse.position = (x,y)

    def press_mouse(self,x = None, y = None, clic_right = False, double_clic = False):
        if x and y:
            self.set_mouse(x,y)
        if clic_right:
            self.mouse.click(Button.right, 1+int(double_clic))
        else:
            self.mouse.click(Button.left, 1+int(double_clic))


