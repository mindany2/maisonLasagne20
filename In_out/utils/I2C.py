from smbus import SMBus
from threading import Lock,Thread
from time import sleep, time
from tree.Tree import Tree
import RPi.GPIO as GPIO

class I2C:
    bus = SMBus(1)
    mutex = Lock()
    temps_reset = time()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(13, GPIO.OUT)

    @classmethod
    def write_reg(self, ip, register, data):
        self.mutex.acquire()
        try:
            self.bus.write_byte_data(ip, register, data)
        except Exception as e:
            print("Erreur sur le bus I2C...."+str(e))
            self.reset_carte_st()
        sleep(0.02)
        self.mutex.release()

    @classmethod
    def write_data(self, ip, data):
        self.mutex.acquire()
        #print("on envoie {} sur le port {}".format(data,ip))
        try:
            self.bus.write_i2c_block_data(ip, 0, data)
        except Exception as e:
            print("Erreur sur le bus I2C...."+str(e))
            print("on a pas pu envoyer {}".format(data))
            self.reset_carte_st()
        sleep(0.02)
        self.mutex.release()

    @classmethod
    def read_reg(self, ip, register): 
        self.mutex.acquire()
        try:
            data = self.bus.read_byte_data(ip, register)
        except Exception as e:
            print("Erreur sur le bus I2C...."+str(e))
            self.reset_carte_st()
            self.mutex.release()
            return None
        sleep(0.02)
        self.mutex.release()
        return data

    @classmethod
    def reset_carte_st(self):
        if time() - self.temps_reset > 10: 
            print("ooooooonnnnnnnnnnn rrrrrrrrrrreeeeeeeeeeeeeesssssssssssssseeeeeeeeeeeeettttttttttt la carte")
            GPIO.output(13, GPIO.LOW)
            sleep(0.01)
            GPIO.output(13, GPIO.HIGH)
            sleep(0.5)
            proc = Thread(target = Tree().refresh_all_projo)
            proc.start()
            self.temps_reset = time()


