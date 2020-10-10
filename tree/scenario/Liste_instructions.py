from tree.scenario.Instruction import Instruction
from threading import Thread, Barrier
from numpy import cumsum
from time import time, sleep
from multiprocessing import Process
from random import random

class Liste_instructions:
    """
    Contient une succession d'instructions
    """
    def __init__(self, boucle, calculateur):
        self.liste = []
        self.liste_barrier = [0]
        self.boucle = boucle
        self.etat = False
        self.id_liste = random()
        self.calculateur = calculateur

    def change_etat(self):
        if self.etat:
            # vire ce scénario
            # on enleve les scénario qu'on a allumer
            for inst in self.liste:
                inst.finish()
        self.etat = not(self.etat)


    def add(self, inst):
        self.liste.append(inst)
        inst.id_liste = self.id_liste
        inst.calculateur = self.calculateur
        self.liste_barrier[-1] += 1
        if not(inst.synchro):
            # on a une nouvelle barrière
            self.liste_barrier.append(0)

    def __eq__(self, other):
        if isinstance(other, Liste_instructions):
            if len(self.liste) == 0 or len(other.liste) == 0:
                return False

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
        while True:
            #on fait toute les instructions
            liste_thread = []
            liste_barrieres = [Barrier(i) for i in self.liste_barrier]
            cummulative_somme = cumsum(self.liste_barrier)
            # on demarre toutes les instructions
            for i,inst in enumerate(self.liste):
                # chaque instruction est un thread
                # on le demarre
                n = sum([int(i+1 > j) for j in cummulative_somme])
                bar = liste_barrieres[n]
                process = Thread(target=inst.run, args=[bar])
                liste_thread.append(process)
                process.start()

            #on attend qu'ils aient tous terminé
            for proc in liste_thread:
                proc.join()
            if not(self.boucle and self.etat):
                break



