from In_out.utils.Spi import Spi
from enum import Enum

class MESSAGE_MASTER(Enum):
    rien = 0
    ferme_trappe = 20
    ouvre_trappe = 21
    relais_led_escalier_on = 22
    relais_led_escalier_off = 23
    sécurité_trappe_on = 24
    sécurité_trappe_off = 25
    demande_etat_trappe = 26

class MESSAGE_SLAVE(Enum):
    rien = 0
    inter_rdc_monte = 5
    inter_rdc_descent = 6
    inter_etage_monte = 7
    inter_etage_descent = 8
    radar_on = 9
    radar_off = 10


class Arduino:
    """
    Classe global, a modifier s'il y en a plusieures
    """
    spi = Spi()
    spi.open(1) # on est sur le port spi1

    @classmethod
    def send(self, message):
        return self.spi.send([message.value])

    @classmethod
    def send_for_request(self, message):
        return self.spi.send_for_request([message.value])
