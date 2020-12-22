from In_out.network.Client import Client
from tree.utils.Locker import Locker
from threading import Thread
from time import sleep,time

TIME_OUT = 10 #s

class Connection(Locker):
    """
    Store connection informations for a network device
    """
    def __init__(self, name, addr):
        Locker.__init__(self)
        self.name = name
        self.addr = addr
        self.client = None
        self.timeout = 0

    def send(self, message):
        self.lock()
        self.timeout = time()
        if not(self.client):
            self.client = Client(self.addr)
            Thread(target=self.check_for_disconnection).start()
        self.client.send(message)
        self.unlock()

    def check_for_disconnection(self):
        """
        check if the connection exceed the TIME_OUT since the last send
        """
        while (time() - self.timeout) < TIME_OUT:
            sleep(1)
        self.disconnect()

    def disconnect(self):
        if self.client:
            self.client.disconnect()
        self.client = None


