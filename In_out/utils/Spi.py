import spidev
from threading import Lock
from time import sleep

class Spi:
    """
    Manage Spi server
    /!\ unused now
    """
    spi = spidev.SpiDev()
    mutex = Lock()

    @classmethod
    def open(self, port):
        self.spi.open(port,0)
        self.spi.max_speed_hz = 10000

    @classmethod
    def send(self, data):
        # /!\ data need to be an integer
        self.mutex.acquire()
        retour = self.spi.xfer(data)
        sleep(0.5)
        self.mutex.release()

    @classmethod
    def send_for_request(self, data):
        self.mutex.acquire()
        self.spi.xfer(data)
        sleep(0.5)
        retour = self.spi.xfer([0])
        sleep(0.5)
        self.mutex.release()
        return retour

    @classmethod
    def close(self):
        self.spi.close()

