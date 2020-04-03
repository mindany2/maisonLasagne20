from spidev import SpiDev
from time import sleep
from threading import Lock

class Bus_vers_STNucleo:
    """
    Ceci est le bus de donnée vers la carte ST
    Nucléo sur les ports correspondant
    """
    bus = SpiDev()
    bus.open(1,0)
    bus.max_speed_hz = 1000000
    mutex = Lock()

    @classmethod
    def write(self, numero_carte, numero_triak, mode):
        data = (numero_carte << 6) + (numero_triak << 2)+mode
        print("on envoie "+ bin(data))
        self.mutex.acquire()
        reponse = self.bus.xfer([data])
        sleep(0.0001)
        reponse = self.bus.xfer([data])
        sleep(0.0001)
        self.mutex.release()
        valeur = reponse[0]
        etat = 1
        print(etat, valeur)
        return (valeur, etat)



