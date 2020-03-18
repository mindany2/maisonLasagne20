from spidev import SpiDev
from time import sleep

class Bus_vers_STNucleo:
    """
    Ceci est le bus de donnée vers la carte ST
    Nucléo sur les ports correspondant
    """
    bus = SpiDev()
    bus.open(1,0)
    bus.max_speed_hz = 1000000

    @classmethod
    def write(self, numero_carte, numero_triak, mode):
        data = (numero_carte << 6) + (numero_triak << 2)+mode
        print("on envoie "+ bin(data))
        reponse = self.bus.xfer([data])
        etat = (reponse[0] & 0b10000000) >> 7
        valeur = reponse[0] & 0b01111111
        print(etat, valeur)
        return (valeur, etat)



