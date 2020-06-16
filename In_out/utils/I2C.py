from smbus import SMBus
from threading import Lock,Thread
from time import sleep

class I2C:
    bus = SMBus(1)
    mutex = Lock()

    @classmethod
    def write_reg(self, ip, register, data):
        self.mutex.acquire()
        try:
            self.bus.write_byte_data(ip, register, data)
        except:
            print("Erreur sur le bus I2C....")
            self.reset_st_carte()
            return 1
        self.mutex.release()
        return 0

    @classmethod
    def write_data(self, ip, data):
        self.mutex.acquire()
        #print("on envoie {} sur le port {}".format(data,ip))
        try:
            self.bus.write_i2c_block_data(ip, 0, data)
        except:
            print("Erreur sur le bus I2C....")
            return 1
        self.mutex.release()
        return 0

    @classmethod
    def read_reg(self, ip, register): 
        self.mutex.acquire()
        try:
            data = self.bus.read_byte_data(ip, register)
        except:
            print("Erreur sur le bus I2C....")
            return None
        self.mutex.release()
        return data


