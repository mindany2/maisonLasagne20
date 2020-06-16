import spidev
from threading import Lock
from time import sleep

class Spi:
    """
    Classe s'occupant de la communication spi MAITRE
    """
    spi = spidev.SpiDev()
    mutex = Lock()

    @classmethod
    def open(self, port):
        # ouvre une connection sur le port demander
        self.spi.open(port,0)
        self.spi.max_speed_hz = 10000

    @classmethod
    def send(self, data):
        # /!\ data doit être un tableau d'entier
        self.mutex.acquire()
        print("on envoie en spi {}".format(data))
        retour = self.spi.xfer(data)
        sleep(0.5)
        self.mutex.release()

    @classmethod
    def send_for_request(self, data):
        self.mutex.acquire()
        print("on envoie en spi {}".format(data))
        self.spi.xfer(data)
        print("on envoie en spi {}".format(0))
        sleep(0.5)
        retour = self.spi.xfer([0])    # pour avoir la valeur de retour
        print("on recoie en spi {}".format(retour))
        sleep(0.5)
        self.mutex.release()
        return retour

    @classmethod
    def close(self):
        self.spi.close()

