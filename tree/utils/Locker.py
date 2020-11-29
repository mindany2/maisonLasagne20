from threading import Lock

class Locker:
    """
    Permet de lock des lumières et périphérique
    et de kill les instructions si necessaire
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
