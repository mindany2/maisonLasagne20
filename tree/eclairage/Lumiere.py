from tree.utils.Locker import Locker
from threading import Lock

class Lumiere(Locker):
    """
    Classe mère de toute les lumières
    """
    def __init__(self, nom):
        Locker.__init__(self)
        self.nom = nom
        self.dimmeur = 0 #éteint
        self.mutex = Lock()

        self.id_scenar = 0
        self.test_lock = 0

    def lock(self, id_liste=0):
        if self.mutex.locked() and id_liste != self.id_scenar:
            # on donne l'ordre de kill the thread en cours
            print("on demande de kill")
            self.test_lock += 1
        self.mutex.acquire()
        self.id_scenar = id_liste
        if self.test_lock > 0:
            self.test_lock -= 1

    def unlock(self):
        self.mutex.release()

    def test(self):
        return self.test_lock > 0
    
    def repair(self):
        return False
        
