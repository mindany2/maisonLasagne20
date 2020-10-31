import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from utils.Logger import Logger
from utils.spotify.Player import Player
from utils.spotify.Track import Track
from tree.Tree import Tree
from threading import Thread
from time import sleep
import os


SCOPE = 'user-read-private,app-remote-control,user-library-read,user-read-currently-playing,user-read-playback-state,user-modify-playback-state,user-top-read'

class Spotify:
    """
    Static class spotify
    utiliser par raspotify
    """
    etat = False
    process = None
    track = None
    volume = 50
    
    PI_ID, ANALYSIS, SCENAR_START, SCENAR_STOP = None, None, None, None
    SCENAR_RELOAD = None

    @classmethod
    def set_pi_id(self, pi_id):
        self.PI_ID = pi_id

    @classmethod
    def set_scenar_stop(self, scenar_stop):
        self.SCENAR_STOP = scenar_stop

    @classmethod
    def get_bpm(self):
        if self.track:
            return self.track.bpm
        return 0

    @classmethod
    def set_scenar_reload(self, scenar):
        self.SCENAR_RELOAD = scenar

    @classmethod
    def set_scenar_start(self, scenar_start):
        self.SCENAR_START = scenar_start

    @classmethod
    def init(self):

        self.token = util.prompt_for_user_token("salle",
                                SCOPE,
                                cache_path = ".cache-salle",
                                client_id = '34eb7c4796fd4c85bd09804bf27011dc',
                                client_secret = '1db71ff1ff9d4dadb071aa85df0a58a3',
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)
        if self.ANALYSIS:
            print("ooooooooooooooooooooooooooooooooooooooooooookkkkkkkkkkkkkkkkkkkk")
            self.player = Player(self.sp)
            self.player.start()
            self.track = None

    @classmethod
    def refresh_token(self):
        self.token = util.prompt_for_user_token("salle",
                                SCOPE,
                                client_id = '34eb7c4796fd4c85bd09804bf27011dc',
                                client_secret = '1db71ff1ff9d4dadb071aa85df0a58a3',
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)

    @classmethod
    def wait_for_beat(self, number):
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
        Logger.debug("Spotify : {} : volume={} : track ={} : position {}".format(status, volume, track, position))
        if status == "start":
            if self.ANALYSIS:
                self.player.start()
                self.track = Track(self.sp, self.player, track)
        elif status == "playing":
            if self.ANALYSIS:
                self.player.start()
                print("music = {} : player = {} : diff = {}".format(position, self.player.temps, int(position)-self.player.temps))
                self.player.set(int(position))
            if not(self.etat) and self.SCENAR_START:
                self.SCENAR_START.do()
            self.etat = True

        elif status == "paused":
            if self.ANALYSIS:
                self.player.stop()
                print("music = {} : player = {} : diff = {}".format(position, self.player.temps, int(position)-self.player.temps))
            if self.etat and self.SCENAR_STOP:
                self.SCENAR_STOP.do()
            self.etat = False

        elif status == "stop":
            if self.ANALYSIS:
                self.player.stop()
            if self.etat and self.SCENAR_STOP:
                self.SCENAR_STOP.do()
            self.etat = False

        elif status == "volume_set":
            # on set le nv volume
            print("nv volume = "+str(volume))
            if abs(volume-self.volume) > 20:
                self.SCENAR_RELOAD.do()
                self.volume = volume


        elif status == "change":
            if self.ANALYSIS:
                track = Track(self.sp, self.player, track)
                if self.track != None:
                    self.track.kill()
                self.track = track

    @classmethod
    def kill(self):
        try:
            self.sp.pause_playback(self.PI_ID)
        except spotipy.exceptions.SpotifyException:
            self.refresh_token()
            self.kill()
        self.etat = False

    @classmethod
    def start(self):
        print("start")
        try:
            self.sp.transfer_playback(self.PI_ID, force_play=True)
            self.sp.repeat("context", device_id=self.PI_ID)
            self.SCENAR_START.do()
        except spotipy.exceptions.SpotifyException:
            self.refresh_token()
            os.system("sudo systemctl restart raspotify.service")
            sleep(2)
            self.start()
        self.etat = True


if __name__ == "__main__":
    spotify = Spotify()
    spotify.init()

