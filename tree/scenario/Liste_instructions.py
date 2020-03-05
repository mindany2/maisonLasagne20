from tree.scenario.Instruction import Instruction
from threading import Thread

class Liste_instructions:
    """
    Contient une succession d'instructions
    """
    def __init__(self):
        self.liste = []

    def add(self, inst):
        self.liste.append(inst)

    def __iter__(self):
        return self.liste.__iter__()

    def do(self):
        #on fait toute les instructions
        liste_thread = []
        for inst in self.liste:
            # chaque instruction est un thread
            # on le demarre
            print("on demarre "+inst.lumière.nom)
            process = Thread(target=inst.run)
            process.start()
            if (inst.attente):
                # on doit attendre que l'instruction se termine
                print("on attent "+inst.lumière.nom)
                process.join()
            else :
                liste_thread.append(process)

        #on attend qu'ils aient tous terminé
        for proc in liste_thread:
            print("on recupére "+inst.lumière.nom)
            proc.join()


