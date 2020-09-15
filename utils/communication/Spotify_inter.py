from utils.spotify.Spotify import Spotify
from utils.communication.Message import Message
from threading import Thread

class Spotify_inter(Message):

    def __init__(self, etat, volume, track, position):
        self.etat = etat
        self.volume = volume
        self.track = track
        self.position = position

    def do(self):
        proc = Thread(target=Spotify.inter, args = [self.etat, self.volume, self.track, self.position])
        proc.start()
