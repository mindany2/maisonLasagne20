from enum import Enum
from threading import Lock
from In_out.utils.I2C import I2C
from time import sleep

class MESSAGE_MASTER(Enum):
    rien = 0
    relais_led_escalier_on = 20
    relais_led_escalier_off = 21
    sécurité_trappe_on = 22
    sécurité_trappe_off = 23
    demande_etat_trappe = 24

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
    ip = 0x10
    mutex = Lock()

    @classmethod
    def send(self, message):
        self.mutex.acquire()
        for i in range(0,5):
            if not(self.i2c.write_data(self.ip, [message.value])):
                break
            sleep(0.5)
        sleep(0.1)
        self.mutex.release()

    @classmethod
    def send_for_request(self, message):
        self.mutex.acquire()
        data = self.i2c.read_reg(self.ip, message.value)
        sleep(0.1)
        self.mutex.release()
        return data
