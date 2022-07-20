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
    This is a bus to talk with the port extender :
    https://tinyurl.com/rpi-port-extender
    """
    def __init__(self):
        self.i2c = I2C()
        self.i2c.start()
        self.mutex = Lock()

    def write(self, ip, register, data):
        self.mutex.acquire()
        self.i2c.write_reg(ip, register, data)
        self.mutex.release()

    def write_pin(self, ip, register, numero, valeur):
        self.mutex.acquire()
        data =  self.i2c.read_reg(ip, register)
        if data == None:
            self.mutex.release()
            return
        data = binbits(data,8)
        data = data[0:(numero-1)]+str(1-valeur)+data[(numero)::]
        data = int(data,2)
        self.i2c.write_reg(ip, register, data)
        self.mutex.release()

    def read(self, ip, register):
        data =  self.i2c.read_reg(ip, register)
        if data != None:
            data = binbits(data, 8)
            return [pin for pin in data]


