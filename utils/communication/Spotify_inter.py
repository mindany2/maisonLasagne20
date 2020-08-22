from tree.utils.Spotify import Spotify
from utils.communication.Message import Message
from threading import Thread

class Spotify_inter(Message):

    def __init__(self, etat):
        self.etat = etat

    def do(self):
        proc = Thread(target=Spotify.inter, args = [self.etat])
        proc.start()
