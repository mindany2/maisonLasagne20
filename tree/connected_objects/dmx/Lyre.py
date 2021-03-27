from tree.connected_objects.dmx.Dmx_device import Dmx_device
from enum import Enum
from tree.utils.Locker import Locker

class Lyre(Dmx_device):
    """
    Fun Generation PicoSpot 20 LED
    https://www.thomann.de/intl/fun_generation_picospot_20_led.htm

    A small lyre with 11 channels
    9 colors
    9 gobos
    """
    def __init__(self, name, relay, addr, dmx):
        Dmx_device.__init__(self, name, relay, addr, dmx)
        self.pan = 0
        self.tilt = 0
        self.speed_motor = 0
        self.speed = 0
        self.strombo = 0
        self.dimmer = 0

        self.color = COLOR.white
        self.gobo = GOBO.simple_round
        
        self.locker_dimmer = Locker()

    def set_position(self, pan, tilt):
        if self.pan != pan:
            super().set(CHANNEL.pan, pan)
        if self.tilt != tilt:
            super().set(CHANNEL.tilt, tilt)
        self.pan = pan
        self.tilt = tilt

    def set_color(self, color):
        if self.color != color:
            super().set(CHANNEL.color, color.value)
        self.color = color

    def set_gobo(self, gobo):
        if self.gobo != gobo:
            super().set(CHANNEL.gobo, gobo.value)
        self.gobo = gobo

    def set_strombo(self, strombo):
        if self.strombo != strombo:
            super().set(CHANNEL.strombo, strombo)
        self.strombo = strombo

    def set_dimmer(self, dimmer):
        if self.dimmer != dimmer:
            super().set(CHANNEL.dimmer, dimmer)
        self.dimmer = dimmer

    def set_speed(self, speed):
        if self.speed != speed:
            super().set(CHANNEL.speed, speed)
        self.speed = speed

    def set_speed_motor(self, speed_motor):
        if self.speed_motor != speed_motor:
            super().set(CHANNEL.speed_motor, speed_motor)
        self.speed_motor = speed_motor

    def get_position(self):
        return (self.pan, self.tilt)

    def lock_dimmer(self):
        self.locker_dimmer.lock()

    def test_dimmer(self):
        return self.locker_dimmer.test()

    def unlock_dimmer(self):
        self.locker_dimmer.unlock()

    def reload(self, other):
        if isinstance(other, Lyre):
            self.pan  = other.pan
            self.tilt = other.tilt
            self.speed_motor = other.speed_motor
            self.strombo = other.strombo
            self.dimmer = other.dimmer
            self.color = other.color
            self.gobo = other.gobo

    def __eq__(self, other):
        if isinstance(other, Lyre):
            return super().__eq__(other)\
                    and self.pan == other.pan\
                    and self.tilt == other.tilt\
                    and self.speed_motor == other.speed_motor\
                    and self.speed == other.speed\
                    and self.strombo == other.strombo\
                    and self.dimmer == other.dimmer\
                    and self.color == other.color\
                    and self.gobo == other.gobo
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : Lyre\n")
        string += "".join("- Dmx : {}\n".format(super()))
        return string

class COLOR(Enum):
    # the full color
    #TODO midle color
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
    # static gobos
    #TODO shaked gobos
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
    # 11 channels
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

