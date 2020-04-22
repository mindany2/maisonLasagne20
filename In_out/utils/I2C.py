from smbus import SMBus
from threading import Lock

class I2C:
    bus = SMBus(1)
    mutex = Lock()

    @classmethod
    def write_reg(self, ip, register, data):
        self.mutex.acquire()
        self.bus.write_byte_data(ip, register, data)
        self.mutex.release()

    @classmethod
    def write_data(self, ip, data):
        self.mutex.acquire()
        #print("on envoie {} sur le port {}".format(data,ip))
        self.bus.write_i2c_block_data(ip, 0, data)
        self.mutex.release()

    @classmethod
    def read_reg(self, ip, register): 
        self.mutex.acquire()
        data = self.bus.read_byte_data(ip, register)
        self.mutex.release()
        return data
