import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tree.utils.Logger import Logger
from data_manager.utils.Secrets import Secrets
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
    def __init__(self, name, secrets, pi_id, scenar_start = None, scenar_stop = None,
                        scenar_volume = None, analysis = False, volume_init = None):
        self.state = False
        self.process = None
        self.track = None
        if volume_init:
            self.volume = volume_init
        else:
            self.volume = 50
        self.analysis = analysis

        self.pi_id = pi_id
        self.name = name
        self.name_scenar_start = scenar_start
        self.name_scenar_stop = scenar_stop
        self.name_scenar_volume = scenar_volume

        self.scenar_start, self.scenar_volume, self.scenar_stop = None, None, None

        self.secrets = secrets
        self.get_token()

    def initialize(self):
        if self.name_scenar_start:
            self.scenar_start = self.name_scenar_start.get_scenarios()
        if self.name_scenar_stop:
            self.scenar_stop = self.name_scenar_stop.get_scenarios()
        if self.name_scenar_volume:
            self.scenar_volume = self.name_scenar_volume.get_scenarios()

    def get_bpm(self):
        if self.track:
            return self.track.bpm
        return 0

    def get_token(self):
        self.token = util.prompt_for_user_token(self.name,
                                SCOPE,
                                cache_path = ".spotipy-cache",
                                client_id = self.secrets.get_str("client_id", mandatory=True),
                                client_secret = self.secrets.get_str("client_secret", mandatory=True),
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)
        if self.analysis:
            self.player = Player(self.sp)
            self.player.start()
            self.track = None

    def refresh_token(self):
        self.token = util.prompt_for_user_token(self.name,
                                SCOPE,
                                cache_path = ".spotipy-cache",
                                client_id = self.secrets.get_str("client_id", mandatory=True),
                                client_secret = self.secrets.get_str("client_secret", mandatory=True),
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

    def inter(self, getter, status, volume, track, position):
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
        except spotipy.exceptions.SpotifyException as e:
            os.system("sudo systemctl restart raspotify.service")
        self.state = False

    def start(self, attemps = 0):
        try:
            self.sp.transfer_playback(self.pi_id, force_play=True)
            self.sp.repeat("context", device_id=self.pi_id)
        except spotipy.exceptions.SpotifyException as e:
            self.refresh_token()
            os.system("sudo systemctl restart raspotify.service")
            sleep(2)
            if attemps < 3:
                self.start(attemps+1)
            else:
                Logger.error("Could not start raspotify : "+str(e))
        self.state = True

