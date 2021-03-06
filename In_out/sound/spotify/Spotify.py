import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tree.utils.Logger import Logger
from data_manager.utils.Secrets import Secrets
from In_out.sound.spotify.Player import Player
from In_out.sound.spotify.Track import Track
from threading import Thread
from time import sleep, time
import os
from In_out.utils.File_management import File_management
from tree.utils.calculs.Variable import Variable


SCOPE = 'user-read-private,app-remote-control,user-library-read,user-read-currently-playing,user-read-playback-state,user-modify-playback-state,user-top-read'

class Spotify:
    """
    Static spotify class, used by the tree and raspotify
    """
    def __init__(self, name, secrets, pi_id, scenar_start = None, scenar_stop = None,
                        scenar_volume = None, analysis = False, volume_init = 40, save_image=None):
        self.state = False
        self.process = None
        self.track = None
        self.save_image = save_image
        self.analysis = analysis

        self.pi_id = pi_id
        self.name = name
        self.name_scenar_start = scenar_start
        self.name_scenar_stop = scenar_stop
        self.name_scenar_volume = scenar_volume

        self.scenar_start, self.scenar_volume, self.scenar_stop = None, None, None
        self.volume = Variable("spotify_volume", volume_init, action_set=self.set_volume, action_get=self.get_volume)

        self.secrets = secrets
        self.get_token()

    def initialize(self):
        if self.name_scenar_start:
            self.scenar_start = self.name_scenar_start.get_scenarios()
        if self.name_scenar_stop:
            self.scenar_stop = self.name_scenar_stop.get_scenarios()
        if self.name_scenar_volume:
            self.scenar_volume = self.name_scenar_volume.get_scenarios()

    def get_variables(self):
        return [self.volume]

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

    def starting(self, track):
        if self.save_image:
            File_management.download(self.sp.track(track)['album']['images'][0]['url'], self.save_image)
        if self.analysis:
            self.player.start()
            self.track = Track(self.sp, self.player, track)
        if self.scenar_start:
            self.scenar_start.do()

    def playing(self, position):
        if self.analysis:
            self.player.start()
            print("music = {} : player = {} : diff = {}".format(position, self.player.tps, int(position)-self.player.tps))
            self.player.set(int(position))
        if not(self.state) and self.scenar_start:
            self.scenar_start.do()

    def pausing(self, position):
        if self.analysis:
            self.player.stop()
            print("music = {} : player = {} : diff = {}".format(position, self.player.tps, int(position)-self.player.tps))
        if self.state and self.scenar_stop:
            self.scenar_stop.do()

    def stoping(self):
        if self.analysis:
            self.player.stop()
        if self.state and self.scenar_stop:
            self.scenar_stop.do()

    def changing_volume(self, volume):
        if self.scenar_volume:
            self.scenar_volume.do()

    def changing_track(self, track):
        if self.save_image:
            File_management.download(self.sp.track(track)['album']['images'][0]['url'], self.save_image)
        if self.analysis:
            track = Track(self.sp, self.player, track)
            if self.track != None:
                self.track.kill()
            self.track = track

    def inter(self, getter, status, volume, track, position):
        Logger.debug("Spotify : {} : volume={} : track ={} : position {}".format(status, volume, track, position))
        if status == "start":
            self.starting(track)
        elif status == "playing":
            self.playing(position)
            self.state = True
        elif status == "paused":
            self.pausing(position)
            self.state = False
        elif status == "stop":
            self.stoping()
            self.state = False
        elif status == "volume_set":
            self.changing_volume(volume)
        elif status == "change":
            self.changing_track(track)

    def get_volume(self):
        try:
            try:
                device = self.sp.current_playback()["device"]
                if device['id'] == self.pi_id:
                    return device["volume_percent"]
                return None
            except TypeError:
                return None
        except spotipy.exceptions.SpotifyException as e:
            Logger.error(e)
            self.refresh_token()


    def set_volume(self, volume):
        try:
            self.sp.volume(volume, device_id=self.pi_id)
        except spotipy.exceptions.SpotifyException as e:
            self.refresh_token()
            Logger.error(e)

    def kill(self):
        if self.state:
            try:
                self.sp.pause_playback(self.pi_id)
            except spotipy.exceptions.SpotifyException:
                os.system("sudo systemctl restart raspotify.service")

    def start(self, attemps = 0):
        if not self.state:
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

