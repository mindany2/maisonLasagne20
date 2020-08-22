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
        self.liste_thread = []

    def add(self, inst):
        self.liste.append(inst)
        self.liste_barrier[-1] += 1
        if not(inst.synchro):
            # on a une nouvelle barrière
            self.liste_barrier.append(0)

    def __eq__(self, other):
        if isinstance(other, Liste_instructions):
            for inst1 in self.liste:
                for inst2 in other.liste:
                    if inst1.eclairage() == inst2.eclairage(): # si elles ont le même eclairage  
                        if not(inst1 == inst2): # si elle finissent pas pareil
                            return False
            return True

        return False



    def __iter__(self):
        return self.liste.__iter__()

    def do(self):
        #on fait toute les instructions
        self.liste_thread = []
        liste_barrieres = [Barrier(i) for i in self.liste_barrier]
        cummulative_somme = cumsum(self.liste_barrier)
        # on demarre toutes les instructions
        for i,inst in enumerate(self.liste):
            # chaque instruction est un thread
            # on le demarre
            n = sum([int(i+1 > j) for j in cummulative_somme])
            bar = liste_barrieres[n]
            process = Thread(target=inst.run, args=[bar])
            self.liste_thread.append(process)
            process.start()

        #on attend qu'ils aient tous terminé
        for proc in self.liste_thread:
            proc.join()


