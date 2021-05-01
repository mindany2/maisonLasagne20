from tree.connected_objects.Connected_object import Connected_object
from tree.connected_objects.Lamp import Lamp
from enum import Enum
from time import sleep
from threading import Lock

class STATE(Enum):
    up = 1
    down = 2
    in_process = 3

class Trap(Connected_object):
    """
    This is a automated trapdoor in the midle of the house to cut the sound between two levels
    It is control with a distributor of compressed air with 2 states
    There are also an magnet when the trap is open to prevent for air issues
    There are also some sensor to securise the process
    """
    def __init__(self,name, relay_distrib_up, relay_distrib_down, relay_magnet, closed_sensor):
        Connected_object.__init__(self, name)
        self.distrib_up = Lamp("distrib_up",relay_distrib_up)
        self.distrib_down = Lamp("distrib_down",relay_distrib_down)
        self.magnet = Lamp("magnet",relay_magnet, invert=True) # the relay is inverted (magnet is by default ON)
        self.closed_sensor = closed_sensor
        state = self.closed_sensor.capture() 
        if state:
            self.state = STATE.up
        else:
            self.state = STATE.down
        print("the trap is {}".format(self.state))

    def get_state(self):
        return self.state

    def set_magnet(self, state):
        self.magnet.set_state(state)

    def go_down(self):
        self.distrib_down.set_state(True)
        sleep(0.5)
        self.distrib_down.set_state(False)

    def go_up(self):
        self.distrib_up.set_state(True)
        sleep(0.5)
        self.distrib_up.set_state(False)

    def change(self, state):
        self.state = state

    def reload(self, other):
        if isinstance(other, Trap):
            self.state == other.state

    def __eq__(self, other):
        if isinstance(other, Trap):
            return super().__eq__(other)\
                    and self.distrib_up == other.distrib_up\
                    and self.distrib_down == other.distrib_down\
                    and self.magnet == other.magnet\
                    and self.closed_sensor == other.closed_sensor\
                    and self.state == other.state
        return False

    def __str__(self):
        string = super().__str__()
        string += "".join("- Type : trap\n")
        return string




