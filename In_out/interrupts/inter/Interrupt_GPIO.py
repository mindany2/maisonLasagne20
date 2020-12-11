from time import time
from tree.Tree import Tree
from In_out.interrupts.inter.Interrupt import Interrupt
from time import sleep
try:
    import RPi.GPIO as GPIO
except (RuntimeError, ModuleNotFoundError):
    import fake_rpigpio.utils
    fake_rpigpio.utils.install()

class Interrupt_GPIO(Interrupt):
    """
    It is a GPIO interrupt
    """
    def __init__(self, name, pin, client):
        Interrupt.__init__(self, name, client)
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(pin, GPIO.BOTH, callback=self.press)
        self.value = GPIO.input(pin)
        if (GPIO.input(pin) == GPIO.LOW): # the interrupts is already on
            sleep(1)
            super().press()

    def press(self, event):
        if (self.value != GPIO.input(event)):
            self.value = GPIO.input(event)
            super().press(state = not(self.value))

    def __str__(self):
        return "type : gpio | pin : {}".format(self.pin)
