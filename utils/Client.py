import socket
import pickle

class Client:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.13"
        self.port = 5555
        self.addr = (self.server, self.port)
        hello = self.connect()
        if hello == None:
            print("erreur de connection")
            raise(Exception)
        print("hello msg : ",hello)

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except:
            print("erreur de connection")

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


    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            data = pickle.loads(self.client.recv(2048))
            if isinstance(data,str):
                if data.count("Error"):
                    print(data)
                    self.client.disconnect()
            return data
        except socket.error as e:
            print(e)
            self.client.disconnect()
        



