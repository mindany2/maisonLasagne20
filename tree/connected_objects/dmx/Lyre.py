from enum import Enum
from threading import Lock
from tree.connected_objects.Lamp import Lamp

class Lyre(Lamp):
    """
    Fun Generation PicoSpot 20 LED
    https://www.thomann.de/intl/fun_generation_picospot_20_led.htm

    A small lyre with 11 channels
    9 colors
    9 gobos
    """
    def __init__(self, name, relay, controler):
        Lamp.__init__(self, name, relay)
        self.dmx = controler
        self.pan = 0
        self.tilt = 0
        self.speed_motor = 0
        self.speed = 0
        self.strombo = 0
        self.dimmer = 0

        self.color = COLOR.white
        self.gobo = GOBO.simple_round
        
        self.mutex_dimmer = Lock()
        self.test_lock_dimmer = 0

    def set_position(self, pan, tilt):
        if self.pan != pan:
            self.dmx.set(CHANNEL.pan, pan)
        if self.tilt != tilt:
            self.dmx.set(CHANNEL.tilt, tilt)
        self.pan = pan
        self.tilt = tilt

    def set_color(self, color):
        if self.color != color:
            self.dmx.set(CHANNEL.color, color.value)
        self.color = color

    def set_gobo(self, gobo):
        if self.gobo != gobo:
            self.dmx.set(CHANNEL.gobo, gobo.value)
        self.gobo = gobo

    def set_strombo(self, strombo):
        if self.strombo != strombo:
            self.dmx.set(CHANNEL.strombo, strombo)
        self.strombo = strombo

    def set_dimmer(self, dimmer):
        if self.dimmer != dimmer:
            self.dmx.set(CHANNEL.dimmer, dimmer)
        self.dimmer = dimmer

    def set_speed(self, speed):
        if self.speed != speed:
            self.dmx.set(CHANNEL.speed, speed)
        self.speed = speed

    def set_speed_motor(self, speed_motor):
        if self.speed_motor != speed_motor:
            self.dmx.set(CHANNEL.speed_motor, speed_motor)
        self.speed_motor = speed_motor

    def get_position(self):
        return (self.pan, self.tilt)

    def lock_dimmer(self):
        if self.mutex_dimmer.locked():
            # on donne l'ordre de kill the thread en cours
            self.test_lock_dimmer += 1
        self.mutex_dimmer.acquire()
        if self.test_lock_dimmer > 0:
            self.test_lock_dimmer -= 1

    def test_dimmer(self):
        return self.test_lock_dimmer>0

    def unlock_dimmer(self):
        self.mutex_dimmer.release()




class COLOR(Enum):
    # il manque les milieux
    white = 0
    red = 15
    orange = 25
    yellow = 37
    green = 50
    blue = 60
    cyan = 70
    purple = 80
    wheel = 255

class GOBO(Enum):
    # il manque les gobos qui bougent
    simple_round = 0
    breaking_round = 20
    flower = 40
    flake = 50
    tag = 65
    dots = 80
    tatoo = 95
    scratch = 110
    wheel = 110

class CHANNEL(Enum):
    pan = 1
    tilt = 2
    ajustment_pan = 3
    ajustment_tilt = 4
    speed_motor = 5
    color = 6
    gobo = 7
    dimmer = 8
    strombo = 9
    scene = 10
    speed = 11

