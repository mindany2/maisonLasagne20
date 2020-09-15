from threading import Thread, Condition
from time import sleep

class Track:
    """
    Retrouve toutes les infos du track
    """

    def __init__(self, sp, player, id_track):
        self.sp = sp
        self.player = player
        self.id = id_track
        self.analysis = self.sp.audio_analysis(self.id)
        self.infos = self.sp.audio_features(self.id)
        self.beat = Condition()
        pc = Thread(target=self.beats_action)
        pc.start()
        
    def kill(self):
        try:
            self.beat.acquire()
            self.beat.notify_all()
        finally:
            self.beat.release()

    def beats_action(self):
        beats = [el["start"] for el in self.analysis["tatums"]]
        print([el["tempo"] for el in self.analysis["sections"]])
        for beat in beats:
            while beat*1000 > self.player.temps:
                sleep(0.0005)
            try:
                self.beat.acquire()
                self.beat.notify_all()
                print("beat !!!!")
            finally:
                self.beat.release()
        print("fin")
