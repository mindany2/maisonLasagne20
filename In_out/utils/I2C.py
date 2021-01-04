from smbus import SMBus
from threading import Lock,Thread
from time import sleep, time
from tree.utils.Logger import Logger

class I2C:

    mutex = Lock()

    @classmethod
    def start(self):
        try:
            self.bus = SMBus(1)
            sleep(0.5)
        except Exception as e:
            Logger.warn("Could not found i2c bus : "+str(e))

    @classmethod
    def write_reg(self, ip, register, data):
        self.mutex.acquire()
        try:
            self.bus.write_byte_data(ip, register, data)
        except Exception as e:
            Logger.error("I2C write reg error : "+str(e))
            self.start()
        sleep(0.1) # to make sure all the infos are sent
        self.mutex.release()

    @classmethod
    def write_data(self, ip, data):
        self.mutex.acquire()
        try:
            self.bus.write_i2c_block_data(ip, 0, data)
        except Exception as e:
            Logger.error("I2C write data error : "+str(e))
            self.start()
            self.mutex.release()
            return 1
        sleep(0.1)
        self.mutex.release()
        return 0

    @classmethod
    def read_reg(self, ip, register): 
        self.mutex.acquire()
        try:
            data = self.bus.read_byte_data(ip, register)
        except Exception as e:
            Logger.error("I2C read reg error : "+str(e))
            self.start()
            self.mutex.release()
            return None
        sleep(0.1)
        self.mutex.release()
        return data

