import spotipy
import spotipy.util as util

from utils.Logger import Logger
from tree.Tree import Tree
from threading import Thread
from time import sleep
import os

PI_ID = 'a21317bcaedc7bea85e391db0af14d059b476c9e'

SCOPE = 'user-read-private,app-remote-control,user-library-read,user-read-currently-playing,user-read-playback-state,user-modify-playback-state,user-top-read'

class Spotify:
    """
    Static class spotify
    utiliser par raspotify
    """
    etat = False
    process = None

    @classmethod
    def init(self):

        print("init")
        self.token = util.prompt_for_user_token("maison",
                                SCOPE,
                                client_id = '34eb7c4796fd4c85bd09804bf27011dc',
                                client_secret = '1db71ff1ff9d4dadb071aa85df0a58a3',
                                redirect_uri = 'http://localhost:8080/')
        print("bloquer")
        self.sp = spotipy.Spotify(auth=self.token)
        print("passer")

    @classmethod
    def inter(self, status, volume):

        etat = self.etat
        Logger.debug("Spotify : {} : volume={}".format(status, volume))
        if status == "playing":
            etat = True
        elif status in ("paused", "stop"):
            etat = False
        elif status == "volume_set":
            # on set le nv volume
            print("nv volume = "+str(volume))

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

    @classmethod
    def kill(self):
        #self.sp.pause_playback(PI_ID)
        os.system("sudo systemctl restart raspotify.service")
        self.etat = False


