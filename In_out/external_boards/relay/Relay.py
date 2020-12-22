from enum import Enum
from threading import Lock

class STATE(Enum):
    ON = 1
    OFF = 0

class Relay:
    """
    This is a simple relay
    """
    def __init__(self):
        self.state = STATE.OFF
        self.nb_objects = 0
        self.mutex = Lock()

    def set(self, state):
        self.mutex.acquire()
        # if there are more than one light in this relay
        # need to be sure all of them is down
        if self.nb_objects <= 1:
            if self.state != state:
                self.state = state
                assert(isinstance(self.state, STATE))
                self.reload()
        self.nb_objects += (2*state.value) - 1
        assert(self.nb_objects >=0)
        self.mutex.release()

    def reload(self):
        # set the relay to the current state
        pass

