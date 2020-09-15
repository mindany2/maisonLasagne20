from time import time, sleep
from threading import Thread, Lock

class Player:
    """
    Bande temporel pour etre toujours
    au bon endroit dans la musique en cours
    """

    def __init__(self, sp):
        self.temps = 0
        self.sp = sp
        self.mutex = Lock()
        self.started = False

    def start(self):
        if not(self.started):
            self.started = True
            proc = Thread(target=self.run)
            proc.start()

    def run(self):
        while self.started:
            # add 1ms
            tps = time()
            while time() - tps < 0.001:
                pass
            self.mutex.acquire()
            self.temps += 1
            self.mutex.release()
        self.continu = True

    def set(self, temps):
        self.mutex.acquire()
        self.temps = temps
        self.mutex.release()

    def stop(self):
        self.started = False


