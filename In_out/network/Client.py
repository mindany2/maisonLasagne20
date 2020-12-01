import socket
import pickle
from threading import Lock
from time import time, sleep
WITH_NETIFACE = True
# threre are trubleshooting installing netifaces
try:
    import netifaces as ni
except:
    WITH_NETIFACE = False

from tree.utils.Logger import Logger

class Client:
    """
    This is a client, it allows to connect to a server on the network
    and send to it messages
    """

    def __init__(self, ip_address = None):
        self.mutex = Lock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not(ip_address): # == None
            if WITH_NETIFACE:
                # use the ip of this rpi
                ni.ifaddresses('eth0')
                self.ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
                Logger.debug("ip addresse = {}".format(self.ip_address))
            else:
                self.ip_address = socket.gethostbyname(socket.gethostname())
        else:
            self.ip_address = ip_address

        self.port = 5555
        self.addr = (self.ip_address, self.port)
        hello = self.connect()
        while hello == None:
            hello = self.connect()
        Logger.debug("hello msg : " + hello)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(8000)) # maybe need to up this value
        except:
            Logger.error("The connection to the server failed")
            sleep(5)

    def send(self, msg):
        try:
            self.mutex.acquire()
            self.client.send(pickle.dumps(msg))
            raw_data = self.client.recv(8000)
            data = ""
            if raw_data != b'':
                data = pickle.loads(raw_data)
            self.mutex.release()
            return data

        except socket.error as e:
            Logger.error(e)

    def disconnect(self):
        self.send("kill me")
        



