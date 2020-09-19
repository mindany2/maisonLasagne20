from tree.scenario.Liste_instructions import Liste_instructions
from threading import Thread
from enum import Enum

class MARQUEUR(Enum):
    """
    Permet de type les scenarios
    """
    OFF = 0
    ON = 1
    DECO = 2

class Scenario:
    """
    La base d'un bouton, juste un état
    """

    def __init__(self, nom, marqueur,calculateur, boucle = False):
        self.nom = nom
        self.liste_inst = Liste_instructions(boucle, calculateur)
        self.marqueur = marqueur

    def __eq__(self, obj):
        if isinstance(obj, Scenario):
            # si les liste_inst finissent pareil
            return self.liste_inst == obj.liste_inst
        return False

    def add_inst(self, inst):
        self.liste_inst.add(inst)

    def get_marqueur(self):
        return self.marqueur

    def etat(self):
        return self.liste_inst.etat

    def change(self):
        self.liste_inst.change_etat()

    def reset(self):
        self.liste_inst.etat = False

    def do(self, join = False):
        proc = Thread(target=self.liste_inst.do)
        proc.start()
        if join:
            proc.join()
        return self

    def show(self):
        print(self.nom)
        for inst in self.liste_inst:
            inst.show()
