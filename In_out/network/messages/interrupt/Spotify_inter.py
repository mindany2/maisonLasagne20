from In_out.network.messages.Message import Message
from threading import Thread

class Spotify_inter(Message):

    def __init__(self, state, volume, track, position):
        self.state = state
        self.volume = volume
        self.track = track
        self.position = position

    def do(self, getter):
        proc = Thread(target=getter.get_spotify().inter, args = [self.state, self.volume, self.track, self.position])
        proc.start()
