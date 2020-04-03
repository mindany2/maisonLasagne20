from tree.scenario.Scenario import Scenario
from threading import Thread, Barrier
from numpy import cumsum

class Liste_scenarios:
    """
    Contient une succession d'instructions
    """
    def __init__(self):
        self.liste = {}

    def add(self, scénar, attente):
        # attente = si on attend la fin du premier scénario pour continuer
        self.liste[scénar] = attente

    def __iter__(self):
        return self.liste.keys().__iter__()

    def do(self):
        liste_thread = []
        for scénar in self.liste.keys():
            attente = self.liste[scénar]
            process = Thread(target = scénar.do)
            process.start()
            if attente:
                process.join()
            else :
                liste_thread.append(process)



