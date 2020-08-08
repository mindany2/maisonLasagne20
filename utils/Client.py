import socket
import pickle
from threading import Lock
from time import time, sleep
import netifaces as ni
from utils.Logger import Logger

class Client:
    mutex = Lock()

    def __init__(self, ip_address = None):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not(ip_address): # == None
            # on utilise l'ip de ce rpi
            ni.ifaddresses('eth0')
            self.ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
            Logger.debug("ip addresse = {}".format(self.ip_address))
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
            return pickle.loads(self.client.recv(2048))
        except:
            Logger.error("erreur de connection au serveur")
            sleep(5)

    def send_request(self, fonction, args = []):
        data = fonction+"("
        for arg in args:
            if isinstance(arg,str):
                data += "\""+arg+"\""
            else:
                data += str(arg)
            data += ","
        data += ")"
        return self.send(data)

    def send(self, msg):
        try:
            self.mutex.acquire()
            self.client.send(pickle.dumps(msg))
            data = pickle.loads(self.client.recv(2048))
            self.mutex.release()
            if isinstance(data,str):
                if data.count("Error"):
                    Logger.error(data)
                    Logger.error("lors de l'envoie de {}".format(msg))
                    return None
            return data
        except socket.error as e:
            Logger.error(e)
        



