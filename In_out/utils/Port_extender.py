from In_out.utils.I2C import I2C
from threading import Lock
from time import sleep

def binbits(x, n):
    """Return binary representation of x with at least n bits"""
    bits = bin(x).split('b')[1]

    if len(bits) < n:
        return '0' * (n - len(bits)) + bits
    return bits

class Port_extender:
    """
    Ceci est le bus de donnée
    vers la carte sur le rasperry pour augmenter le
    nombre de ports
    """
    #TODO passer en non-static en utilisant le gestionnaire de cartes
    i2c = I2C()
    mutex = Lock()

    @classmethod
    def write(self, ip, register, data):
        self.mutex.acquire()
        self.i2c.write_reg(ip, register, data)
        self.mutex.release()
        #print("on ecrit donc "+bin(data) + " dans resgistre "+hex(register)+" ip "+hex(ip))

    @classmethod
    def write_pin(self, ip, register, numero, valeur):
        self.mutex.acquire()
        data =  self.i2c.read_reg(ip, register)
        print("on a lut {}".format(data))
        data = binbits(data,8)
        data = data[0:(numero-1)]+str(1-valeur)+data[(numero)::]
        print("on ecrit donc "+data + " dans resgistre "+hex(register)+" ip "+hex(ip))
        data = int(data,2)
        self.i2c.write_reg(ip, register, data)
        self.mutex.release()

    @classmethod
    def read(self, ip, register):
        data =  self.i2c.read_reg(ip, register)
        if data != None:
            data = binbits(data, 8)
            #print("data = {}".format(data))
            return [pin for pin in data]


