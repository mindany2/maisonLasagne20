import socket
import pickle
from threading import Lock
from time import time, sleep

from tree.utils.Logger import Logger

class Client:
    """
    This is a client, it allows to connect to a server on the network
    and send to it messages
    """

    def __init__(self, ip_address = None):
        self.mutex = Lock()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not(ip_address):
            ip_address = self.get_device_ip()
        self.ip_address = ip_address
        self.port = 5555
        self.addr = (self.ip_address, self.port)
        self.connected = False

    def get_device_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def start(self):
        hello = self.connect()
        while hello == None:
            hello = self.connect()
        Logger.debug("hello msg : " + hello)

    def connect(self):
        self.client.connect(self.addr)
        try:
            self.connected = True
            return pickle.loads(self.client.recv(8000)) # maybe need to up this value
        except :
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

    def state(self):
        return self.connected

    def disconnect(self):
        self.send("kill me")
        self.connected = False
        



