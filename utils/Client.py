import socket
import pickle
from threading import Lock
from time import time, sleep

class Client:
    mutex = Lock()
    temps = 0

    def __init__(self, ip_address = "192.168.1.20"):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if not(ip_address): # == None
            # on utilise l'ip de ce rpi
            hostname = socket.gethostname()
            self.ip_address = socket.gethostbyname(hostname)
        else:
            self.ip_address = ip_address

        self.port = 5555
        self.addr = (self.ip_address, self.port)
        hello = self.connect()
        while hello == None:
            hello = self.connect()
        print("hello msg : ",hello)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            print("erreur de connection au serveur")
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
            debut = time()
            self.client.send(pickle.dumps(msg))
            data = pickle.loads(self.client.recv(2048))
            self.temps += time() -debut
            print(self.temps)
            self.mutex.release()
            if isinstance(data,str):
                if data.count("Error"):
                    print(data)
                    print("lors de l'envoie de {}".format(msg))
                    return None
            return data
        except socket.error as e:
            print(e)
        



