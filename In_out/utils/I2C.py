from smbus import SMBus
from threading import Lock,Thread
from time import sleep, time
from utils.Logger import Logger

class I2C:
    try:
        bus = SMBus(1)
    except:
        Logger.warn("pas de bus i2c")
    mutex = Lock()
    temps_reset = time()

    @classmethod
    def write_reg(self, ip, register, data):
        self.mutex.acquire()
        try:
            self.bus.write_byte_data(ip, register, data)
        except Exception as e:
            Logger.error("Erreur sur le bus I2C...."+str(e))
        sleep(0.02)
        self.mutex.release()

    @classmethod
    def write_data(self, ip, data):
        self.mutex.acquire()
        #print("on envoie {} sur le port {}".format(data,ip))
        try:
            self.bus.write_i2c_block_data(ip, 0, data)
        except Exception as e:
            Logger.error("Erreur sur le bus I2C...."+str(e))
            Logger.error("on a pas pu envoyer {}".format(data))
            self.mutex.release()
            return 1
        sleep(0.02)
        self.mutex.release()
        return 0

    @classmethod
    def read_reg(self, ip, register): 
        self.mutex.acquire()
        try:
            data = self.bus.read_byte_data(ip, register)
        except Exception as e:
            Logger.error("Erreur sur le bus I2C...."+str(e))
            self.mutex.release()
            return None
        sleep(0.02)
        self.mutex.release()
        return data

