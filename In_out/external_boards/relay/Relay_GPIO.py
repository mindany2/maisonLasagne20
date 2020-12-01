from In_out.utils.Arduino import Arduino, MESSAGE_MASTER
from In_out.external_boards.relay.Relay import Relay
from enum import Enum
import RPi.GPIO as GPIO

class Relay_GPIO(Relay):
    """
    It is a relay control directly with the GPIO ports
    """
    def __init__(self, pin):
        Relay.__init__(self)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)
        self.pin = pin

    def reload(self):
        GPIO.output(self.pin,(self.state.value * GPIO.LOW) + (not(self.state.value) *  GPIO.HIGH))
