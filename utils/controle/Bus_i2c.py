from smbus import SMBus
from threading import Lock

def binbits(x, n):
    """Return binary representation of x with at least n bits"""
    bits = bin(x).split('b')[1]

    if len(bits) < n:
        return '0' * (n - len(bits)) + bits
    return bits

class Bus_ports_extender:
    """
    Ceci est le bus de donnée
    vers la carte sur le rasperry pour augmenter le
    nombre de ports
    """
    bus = SMBus(1)
    mutex = Lock()
    for i in range(0x20, 0x28):
        bus.write_byte_data(i, 0x00, 0x00)
        bus.write_byte_data(i, 0x01, 0x00)
        bus.write_byte_data(i, 0x12, 0xff)
        bus.write_byte_data(i, 0x13, 0xff)


    @classmethod
    def write(self, port_bus, register, data):
        self.bus.write_byte_data(port_bus, register, data)

    @classmethod
    def write_pin(self, port_bus, register, numero, valeur):
        self.mutex.acquire()
        data =  self.bus.read_byte_data(port_bus, register)
        data = binbits(data,8)
        data = data[0:(numero-1)]+str(1-valeur)+data[(numero)::]
        print("on ecrit donc "+data + " dans resgistre "+hex(register)+" port "+hex(port_bus))
        data = int(data,2)
        self.write(port_bus, register, data)
        self.mutex.release()


    @classmethod
    def read(self, port_bus, register):
        data =  self.bus.read_byte_data(port_bus, register)
        data = binbits(data, 8)
        for pin in data[2::]:
            yield pin


