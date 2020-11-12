from utils.communication.Client import Client
from tree.utils.Locker import Locker
from threading import Thread
from time import sleep,time

TIME_OUT = 10 #s

class Connection(Locker):
    """
    Stocke les informations de d'un périphérique distant (rpi, pc..)
    """
    def __init__(self, nom, addr):
        Locker.__init__(self)
        self.nom = nom
        self.addr = addr
        self.client = None
        self.timeout = 0

    def send(self, message):
        self.lock()
        self.timeout = time()
        if not(self.client):
            self.client = Client(self.addr)
            Thread(target=self.check_for_deconnection).start()
        self.client.send(message)
        self.unlock()

    def check_for_deconnection(self):
        """
        verifie si la connection n'a pas dépasser TIME_OUT secondes
        depuis le dernier envoi
        """
        while (time() - self.timeout) < TIME_OUT:
            sleep(1)
        if self.client:
            self.client.deconnect()
        self.client = None

