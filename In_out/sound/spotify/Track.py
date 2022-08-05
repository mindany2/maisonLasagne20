from threading import Thread, Condition
from multiprocessing import Process
from time import sleep
import numpy as np
import os

class Track:
    """
    Get all needed infos for a track
    """

    def __init__(self, sp, id_track=""):
        self.sp = sp
        self.id = id_track
        self.bpm = 1
        self.beat = Condition()
        self.running = False

    def change_id(self, id_track):
        self.id = id_track
        self.running = False

    def get_image(self, quality=0):
        assert(quality<3), "Quality must be in 0,2"
        return self.sp.track(self.id)['album']['images'][quality]['url']

    def start_analysis(self, player):
        self.player = player
        self.analysis = self.sp.audio_analysis(self.id)
        self.infos = self.sp.audio_features(self.id)[0]
        self.calcul_beats()
        print(self.infos)
        self.bpm = float(self.infos["tempo"])
        self.running = True

        pc = Thread(target=self.beats_action)
        pc.start()

    def calcul_beats(self):
        self.pitches = [el["pitches"][1]*100 for el in self.analysis['segments']]
        self.start = [el["start"] for el in self.analysis["segments"]]
        tatum = [el["start"] for el in self.analysis["tatums"]]
        self.beats = [el["start"] for el in self.analysis["beats"]]
        decal = self.start[-1]/len(tatum)
        moyenne = np.mean(self.pitches)
        liste = []
        for tat in self.beats:
            val = []
            for i, tps in enumerate(self.start):
                if tps < tat + decal and tps > tat - decal:
                    val.append(self.pitches[i])
            if np.mean(val) > moyenne/2:
                liste.append(1)
            else:
                liste.append(0)
        groupe = [1]
        for i in range(0,len(liste)-3):
            if liste[i+1] == 1 or liste[i+2] == 1:
                groupe[-1] += 1
            elif groupe[-1] > 10 and liste[i+3] == 1:
                groupe[-1] += 1
            else:
                groupe.append(1)

        self.boom = []
        index = 0
        for gp in groupe:
            if gp > 15:
                for i in range(gp):
                    #if liste[i+index] == 1 or liste[i+index-1] == 1 or liste[i+index+1] == 1:
                    self.boom.append(self.beats[i+index])
            index += gp

    def beats_action(self):
        print([el["tempo"] for el in self.analysis["sections"]])
        for beat in self.beats:
            while beat*1000 > self.player.tps and self.running:
                sleep(0.0005)
            self.beat.acquire()
            try:
                self.beat.notify_all()
                print("beat !!!!")
            finally:
                self.beat.release()
            if not self.running:
                break
        print("fin")
