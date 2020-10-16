from threading import Thread, Condition
from multiprocessing import Process
from time import sleep
import numpy as np
import os

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
        self.calcul_beats()
        pc = Thread(target=self.beats_action)
        pc.start()
        
    def kill(self):
        try:
            self.beat.acquire()
            self.beat.notify_all()
        finally:
            self.beat.release()

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
            while beat*1000 > self.player.temps:
                sleep(0.0005)
            try:
                self.beat.acquire()
                self.beat.notify_all()
                print("beat !!!!")
            finally:
                self.beat.release()
        print("fin")
