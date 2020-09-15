from threading import Lock

class Lumiere:
    """
    Classe mère de toute les lumières
    """
    def __init__(self, nom):
        self.nom = nom
        self.dimmeur = 0 #éteint
        self.mutex = Lock()

        self.test_lock = 0

    def lock(self):
        if self.mutex.locked():
            # on donne l'ordre de kill the thread en cours
            self.test_lock += 1
        self.mutex.acquire()
        if self.test_lock > 0:
            self.test_lock -= 1

    def unlock(self):
        self.mutex.release()

    def test(self):
        return self.test_lock > 0
    
