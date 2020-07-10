import socket
import pickle
from threading import Lock
from time import time, sleep

class Client:
    mutex = Lock()
    temps = 0

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.20"
        self.port = 5555
        self.addr = (self.server, self.port)
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
        



