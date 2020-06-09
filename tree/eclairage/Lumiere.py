from threading import Lock

class Lumiere:
    """
    Classe mère de toute les lumières
    """
    def __init__(self, nom):
        self.nom = nom
        self.dimmeur = 0 #éteint
        self.mutex = Lock()

    def lock(self):
        self.mutex.acquire()

    def unlock(self):
        self.mutex.release()
    
