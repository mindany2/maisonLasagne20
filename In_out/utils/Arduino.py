from enum import Enum
from threading import Lock
from In_out.utils.I2C import I2C
from time import sleep

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
    i2c = I2C()
    ip = 0x30
    mutex = Lock()

    @classmethod
    def send(self, message):
        self.mutex.acquire()
        #self.i2c.write_data(self.ip, [message.value])
        if message == MESSAGE_MASTER.ferme_trappe or message == MESSAGE_MASTER.ouvre_trappe:
            sleep(2) # temps de l'instruction
        sleep(0.01)
        self.mutex.release()

    @classmethod
    def send_for_request(self, message):
        #return self.i2c.read_reg(self.ip, message.value)
        pass
