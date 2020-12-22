import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tree.utils.Logger import Logger
from In_out.utils.Secrets import Secrets
from In_out.sound.spotify.Player import Player
from In_out.sound.spotify.Track import Track
from tree.Tree import Tree
from threading import Thread
from time import sleep
import os


SCOPE = 'user-read-private,app-remote-control,user-library-read,user-read-currently-playing,user-read-playback-state,user-modify-playback-state,user-top-read'

class Spotify:
    """
    Static spotify class, used by the tree and raspotify
    """
    def __init__(self, name, pi_id, scenar_start = None, scenar_stop = None,
                        scenar_volume = None, analysis = False, volume_init = 50):
        self.state = False
        self.process = None
        self.track = None
        self.volume = volume_init
        self.analysis = analysis

        self.pi_id = pi_id
        self.name = name
        self.scenar_start = scenar_start
        self.scenar_stop = scenar_stop
        self.scenar_volume = scenar_volume

        # get secrets
        self.secrets = Secrets().get_spotify_secret()
    
    def get_bpm(self):
        if self.track:
            return self.track.bpm
        return 0


    def get_token(self):
        self.token = util.prompt_for_user_token(self.name,
                                SCOPE,
                                #cache_path = ".spotipy-cache",
                                client_id = self.secrets["client_id"],
                                client_secret = self.secrets["client_secret"],
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)
        if self.analysis:
            self.player = Player(self.sp)
            self.player.start()
            self.track = None

    def refresh_token(self):
        self.token = util.prompt_for_user_token("salle",
                                SCOPE,
                                client_id = '34eb7c4796fd4c85bd09804bf27011dc',
                                client_secret = '1db71ff1ff9d4dadb071aa85df0a58a3',
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)

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

    def inter(self, status, volume, track, position):
        Logger.debug("Spotify : {} : volume={} : track ={} : position {}".format(status, volume, track, position))
        if status == "start":
            if self.analysis:
                self.player.start()
                self.track = Track(self.sp, self.player, track)
        elif status == "playing":
            if self.analysis:
                self.player.start()
                print("music = {} : player = {} : diff = {}".format(position, self.player.tps, int(position)-self.player.tps))
                self.player.set(int(position))
            if not(self.state) and self.scenar_start:
                self.scenar_start.do()
            self.state = True

        elif status == "paused":
            if self.analysis:
                self.player.stop()
                print("music = {} : player = {} : diff = {}".format(position, self.player.tps, int(position)-self.player.tps))
            if self.state and self.scenar_stop:
                self.scenar_stop.do()
            self.state = False

        elif status == "stop":
            if self.analysis:
                self.player.stop()
            if self.state and self.scenar_stop:
                self.scenar_stop.do()
            self.state = False

        elif status == "volume_set":
            # on set le nv volume
            print("nv volume = "+str(volume))
            if abs(volume-self.volume) > 20:
                self.scenar_volume.do()
                self.volume = volume


        elif status == "change":
            if self.analysis:
                track = Track(self.sp, self.player, track)
                if self.track != None:
                    self.track.kill()
                self.track = track

    def kill(self):
        try:
            self.sp.pause_playback(self.pi_id)
        except spotipy.exceptions.SpotifyException:
            self.refresh_token()
            self.kill()
        self.state = False

    def start(self):
        print("start")
        try:
            self.sp.transfer_playback(self.pi_id, force_play=True)
            self.sp.repeat("context", device_id=self.pi_id)
            self.scenar_start.do()
        except spotipy.exceptions.SpotifyException:
            self.refresh_token()
            os.system("sudo systemctl restart raspotify.service")
            sleep(2)
        self.state = True

