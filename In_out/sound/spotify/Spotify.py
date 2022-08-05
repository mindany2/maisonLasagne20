import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tree.utils.Logger import Logger
from data_manager.utils.Secrets import Secrets
from In_out.sound.spotify.Player import Player
from In_out.sound.spotify.Track import Track
from In_out.sound.spotify.Utils import SP
from threading import Thread
from time import sleep, time
import os
from In_out.utils.File_management import File_management
from tree.utils.calculs.Variable import Variable



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
        self.name_scenar_start = scenar_start
        self.name_scenar_stop = scenar_stop
        self.name_scenar_volume = scenar_volume
        self.infos = {}

        self.scenar_start, self.scenar_volume, self.scenar_stop = None, None, None
        self.volume = Variable("spotify_volume", volume_init, action_set=self.set_volume, action_get=self.get_volume)
        self.bpm = Variable("bpm", 1, action_get=self.get_bpm)

        self.sp = SP(name, pi_id, secrets)
        if self.analysis:
            self.player = Player(self.sp)
            self.track = Track(self.sp)

    def initialize(self):
        if self.name_scenar_start:
            self.scenar_start = self.name_scenar_start.get_scenarios()
        if self.name_scenar_stop:
            self.scenar_stop = self.name_scenar_stop.get_scenarios()
        if self.name_scenar_volume:
            self.scenar_volume = self.name_scenar_volume.get_scenarios()

    def get_variables(self):
        return [self.volume, self.bpm]

    def get_bpm(self):
        if self.track:
            return self.track.bpm
        return 0

    def add_state(self, name, info):
        # allow to send infos with states
        type, *args = str(info).split(",")
        if type in ["current_track_image","playlist_image"]:
            infos = {"type": type}
            for val in args:
                infos[val.split("=")[0]] = val.split("=")[1]
            self.infos[name] = infos
        else:
            info.raise_error(f"'{info}' is not a spotify info, try 'current_track_image'")

    def get_states(self):
        all_states = {}
        for name, info in zip(self.infos, self.infos.values()):
            try:
                quality = int(info["quality"])
            except ValueError:
                quality = 0
            if info["type"] == "current_track_image":
                if self.track:
                    all_states[name] = {"value": True,"image":self.track.get_image(quality=quality)}
            elif info["type"] == "playlist_image":
                all_states[name] = {"value":True, "image": self.sp.get_playlist(info["id"])["images"][quality]["url"]}
        return all_states

    def wait_for_beat(self, number):
        if self.track != None:
            for _ in range(number):
                self.track.beat.acquire()
                self.track.beat.wait()
                self.track.beat.release()
                if self.track == None:
                    break
        else:
            sleep(0.1)

    def starting(self, track):
        self.track.change_id(track)
        if self.analysis:
            self.player.start()
            self.track.start_analysis(self.player)
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
        self.track.change_id(track)
        if self.analysis:
            self.track.start_analysis(self.player)

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
            device = self.sp.current_playback()["device"]
            if device['id'] == self.pi_id:
                return device["volume_percent"]
            return None
        except TypeError:
            return None

    def set_volume(self, volume):
        self.sp.volume(volume)

    def next_track(self):
        self.sp.next_track()

    def kill(self):
        if self.state:
            try:
                self.sp.pause_playback()
            except spotipy.exceptions.SpotifyException:
                os.system("sudo systemctl restart raspotify.service")

    def start(self, attemps = 0, context_uri = None):
        print(f"start spotify {self.state}, {context_uri}")
        if not(self.state) or context_uri:
            try:
                self.sp.start_playback(context_uri=context_uri)
                self.sp.repeat("context")
            except spotipy.exceptions.SpotifyException as e:
                os.system("sudo systemctl restart raspotify.service")
                sleep(2)
                if attemps < 3:
                    self.start(attemps+1)
                else:
                    Logger.error("Could not start raspotify : "+str(e))

