from time import time, sleep
from threading import Thread, Lock

class Player:
    """
    Temporal line, to be always at the same time
    than the currnt music 
    """

    def __init__(self, sp):
        self.tps = 0
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
            self.tps += 1
            self.mutex.release()
        self.continu = True

    def set(self, tps):
        self.mutex.acquire()
        self.tps = tps
        self.mutex.release()

    def stop(self):
        self.started = False


