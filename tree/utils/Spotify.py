from utils.Logger import Logger
from tree.Tree import Tree
from threading import Thread
from time import sleep

class Spotify:
    """
    Static class spotify
    utiliser par raspotify
    """
    etat = False
    process = None

    @classmethod
    def inter(self, status):
        Logger.debug("Spotify : " + status)
        etat = (status == "playing")
        if etat != self.etat:
            if etat:
                process = Thread(target=Tree().reload_son, args=[etat])
                process.start()
            else:
                self.process = Thread(target=self.inst)
                self.process.start()
        self.etat = etat



    @classmethod
    def inst(self):
        print("on attend")
        sleep(30)
        if not(self.etat):
            Tree().reload_son(False)
            self.etat = False



