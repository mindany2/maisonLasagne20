from In_out.sensors.Sensor import Sensor
import RPi.GPIO as GPIO
from time import sleep,time

class Sensor_GPIO(Sensor):
    
    def __init__(self, name, pin):
        Sensor.__init__(self, name)
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.capture()

    def capture(self):
        self.state = GPIO.input(self.pin)
        return self.state

    def wait_until_change(self, time_out):
        state = self.state
        temps = time()
        while (state == self.state and ((time()-temps) < time_out)):
            self.capture()
            sleep(0.2)

