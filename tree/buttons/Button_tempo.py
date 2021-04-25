from tree.buttons.Button import Button
from threading import Thread
from time import time, sleep

class Button_tempo(Button):
    """
    Button that make a temporal timing between two scenario
    with reset point (if the button is call again)
    """
    def __init__(self, name, manager, scenar_on, scenar_off, tempo):
        Button.__init__(self, name, manager)
        self.scenar_on = scenar_on
        self.scenar_off = scenar_off
        self.tempo = tempo
        self.started = False
        self.time = time()

    def state(self):
        return self.manager.get_state()

    def press(self, state = None):
        if not self.started:
            self.manager.do_scenar_principal(self.scenar_on)
            self.time = time()
            process = Thread(target=self.wait)
            process.name = "Wait tempo button {self.name}"
            process.start()
            self.started = True
        self.time = time()


    def wait(self):
        while time() - self.time < self.tempo:
            sleep(0.1)
        self.manager.do_scenar_principal(self.scenar_off)
        self.started = False

    def __eq__(self, other):
        if isinstance(other, Button_tempo):
            return super().__eq__(other)\
                    and self.scenar_on == other.scenar_on\
                    and self.scenar_off == other.scenar_off\
                    and self.tempo == other.tempo
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : tempo\n")
        string += "".join(f"- tempo : {self.tempo}\n")
        string += "".join("- ON : {}\n".format(self.scenar_on.name))
        if self.scenar_off:
            string += "".join("- OFF : {}\n".format(self.scenar_off.name))
        return string



