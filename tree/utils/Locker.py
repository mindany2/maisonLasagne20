from threading import Lock

class Locker:
    """
    Allow the connected_objects to be use by only one
    thread, but also to be kill if another thread need it
    """
    def __init__(self):
        self.mutex = Lock()
        self.killer = False

    def lock(self):
        self.mutex.acquire()
        self.killer = False

    def unlock(self):
        self.mutex.release()

    def test(self):
        return self.killer
    
    def kill(self):
        self.killer = True
