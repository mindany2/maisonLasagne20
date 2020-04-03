from tree.scenario.Instruction import Instruction
from threading import Thread, Barrier
from numpy import cumsum
from time import time, sleep

class Liste_instructions:
    """
    Contient une succession d'instructions
    """
    def __init__(self):
        self.liste = []
        self.liste_barrier = [0]

    def add(self, inst):
        self.liste.append(inst)
        self.liste_barrier[-1] += 1
        if not(inst.synchro):
            # on a une nouvelle barrière
            self.liste_barrier.append(0)

    def __iter__(self):
        return self.liste.__iter__()

    def do(self):
        #on fait toute les instructions
        liste_thread = []
        print("liste barrier = ", self.liste_barrier)
        liste_barrieres = [Barrier(i) for i in self.liste_barrier]
        cummulative_somme = cumsum(self.liste_barrier)
        temps_prec = 0
        for i,inst in enumerate(sorted(self.liste, key= lambda x: x.temps_init)):
            sleep(inst.temps_init-temps_prec)
            # chaque instruction est un thread
            # on le demarre
            n = sum([int(i+1 > j) for j in cummulative_somme])
            bar = liste_barrieres[n]
            process = Thread(target=inst.run, args=[bar])
            liste_thread.append(process)
            process.start()
            temps_prec = inst.temps_init

        #on attend qu'ils aient tous terminé
        for proc in liste_thread:
            proc.join()


