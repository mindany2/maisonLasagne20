import spotipy
import spotipy.util as util

from utils.Logger import Logger
from utils.spotify.Player import Player
from utils.spotify.Track import Track
from tree.Tree import Tree
from threading import Thread
from time import sleep
import os

PI_ID = "c8539be07e8d3f7c4b809b3509f9f634260643c2"

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

        self.token = util.prompt_for_user_token("salle",
                                SCOPE,
                                client_id = '34eb7c4796fd4c85bd09804bf27011dc',
                                client_secret = '1db71ff1ff9d4dadb071aa85df0a58a3',
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)
        self.player = Player(self.sp)
        self.player.start()
        self.track = None

    @classmethod
    def wait_for_beat(self, number):
        print(self.track)
        if self.track != None:
            cond = self.track.beat
            try:
                cond.acquire()
                for _ in range(number):
                    cond.wait()
                    if self.track == None:
                        break
            finally:
                cond.release()
        else:
            sleep(0.1)

    @classmethod
    def inter(self, status, volume, track, position):
        etat = self.etat
        Logger.debug("Spotify : {} : volume={} : track ={} : position {}".format(status, volume, track, position))
        if status == "start":
            self.player.start()
            self.track = Track(self.sp, self.player, track)
        elif status == "playing":
            etat = True
            self.player.start()
            print("music = {} : player = {} : diff = {}".format(position, self.player.temps, int(position)-self.player.temps))
            self.player.set(int(position))

        elif status == "paused":
            self.player.stop()
            etat = False
            print("music = {} : player = {} : diff = {}".format(position, self.player.temps, int(position)-self.player.temps))

        elif status == "stop":
            etat = False
            self.player.stop()

        elif status == "volume_set":
            # on set le nv volume
            print("nv volume = "+str(volume))

        elif status == "change":
            track = Track(self.sp, self.player, track)
            if self.track != None:
                self.track.kill()
            self.track = track

        if etat != self.etat:
            if etat:
                process = Thread(target=Tree().reload_son, args=[etat])
                process.start()
            else:
                self.process = Thread(target=self.inst)
                self.process.start()
        self.etat = etat

    @classmethod
    def get_bpm(self):
        if self.track:
            return self.track.bpm
        return 0

    @classmethod
    def inst(self):
        print("on attend")
        sleep(30)
        if not(self.etat):
            Tree().reload_son(False)
            self.etat = False

    @classmethod
    def kill(self):
        self.sp.pause_playback(PI_ID)
        self.etat = False

if __name__ == "__main__":
    spotify = Spotify()
    spotify.init()

