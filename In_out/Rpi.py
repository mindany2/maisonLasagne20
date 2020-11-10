from utils.communication.Client import Client
from threading import Thread
from time import sleep,time

TIME_OUT = 10 #s

class Rpi:
    """
    Stocke les informations d'un raspberry distant
    """
    def __init__(self, nom, addr):
        self.nom = nom
        self.addr = addr
        self.client = None
        self.timeout = 0

    def send(self, message):
        if not(self.client):
            self.client = Client(self.addr)
            Thread(target=self.check_for_deconnection).start()
        self.client.send(message)
        self.timeout = time()

    def check_for_deconnection(self):
        """
        verifie si la connection n'a pas dépasser TIME_OUT secondes
        depuis le dernier envoi
        """
        while (time() - self.timeout) < TIME_OUT:
            sleep(1)
        self.client.deconnect()
        self.client = None

