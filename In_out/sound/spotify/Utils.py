import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from tree.utils.Logger import Logger
from time import sleep

def token_check(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except spotipy.exceptions.SpotifyException as e:
            args[0].refresh_token()
            Logger.error(e)
            sleep(0.2)
            return func(*args, **kwargs)
    return wrapper


SCOPE = 'user-read-private,app-remote-control,user-library-read,user-read-currently-playing,user-read-playback-state,user-modify-playback-state,user-top-read'

class SP:
    """
    Manage the connect with the spotify api
    """
    def __init__(self, name, pi_id, secrets):
        self.name = name
        self.pi_id = pi_id
        self.secrets = secrets
        self.get_token()

    def get_token(self):
        self.token = util.prompt_for_user_token(self.name,
                                SCOPE,
                                cache_path = ".spotipy-cache",
                                client_id = self.secrets.get_str("client_id", mandatory=True),
                                client_secret = self.secrets.get_str("client_secret", mandatory=True),
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)

    def refresh_token(self):
        print("refresh  token")
        self.token = util.prompt_for_user_token(self.name,
                                SCOPE,
                                cache_path = ".spotipy-cache",
                                client_id = self.secrets.get_str("client_id", mandatory=True),
                                client_secret = self.secrets.get_str("client_secret", mandatory=True),
                                redirect_uri = 'http://localhost:8888/callback')
        self.sp = spotipy.Spotify(auth=self.token)

    @token_check
    def volume(self, volume):
        self.sp.volume(volume, device_id=self.pi_id)

    @token_check
    def current_playback(self):
        return self.sp.current_playback()

    @token_check
    def pause_playback(self):
        self.sp.pause_playback(self.pi_id)

    @token_check
    def start_playback(self, context_uri=None):
        self.sp.start_playback(self.pi_id, context_uri=context_uri)
        print("started")

    @token_check
    def next_track(self):
        self.sp.next_track(device_id=self.pi_id)

    @token_check
    def repeat(self, mode= "context"):
        self.sp.repeat("context", device_id=self.pi_id)

    @token_check
    def track(self, id):
        return self.sp.track(id)

    @token_check
    def get_playlist(self,id):
        return self.sp.playlist(id)
