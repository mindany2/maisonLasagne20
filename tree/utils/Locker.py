from threading import Lock

class Locker:
    """
    Allow the connected_objects to be use by only one
    thread, but also to be kill if another thread need it
    """
    def __init__(self):
        self.mutex = Lock()
        self.mutex_killer = Lock()
        self.killer = False

    def lock(self):
        if not(self.killer) and self.mutex.locked():
            self.kill()
        self.mutex.acquire()
        self.mutex_killer.acquire()
        self.killer = False
        self.mutex_killer.release()

    def unlock(self):
        self.mutex.release()

    def test(self):
        return self.killer
    
    def kill(self):
        self.mutex_killer.acquire()
        self.killer = True
        self.mutex_killer.release()
