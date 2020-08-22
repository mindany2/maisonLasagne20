from utils.Logger import Logger
from tree.Tree import Tree
from multiprocessing import Process
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
                if self.process:
                    self.process.terminate()
                process = Process(target=Tree().reload_son, args=[etat])
                process.start()
            else:
                self.process = Process(target=self.inst)
                self.process.start()
        self.etat = etat



    @classmethod
    def inst(self):
        print("on attend")
        sleep(30)
        Tree().reload_son(False)
        self.etat = False



