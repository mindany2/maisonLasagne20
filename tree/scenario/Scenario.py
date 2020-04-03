from tree.scenario.Liste_instructions import Liste_instructions
from threading import Thread

class Scenario:
    """
    La base d'un bouton, juste un état
    """

    def __init__(self, nom):
        self.nom = nom
        self.liste_inst = Liste_instructions()

    def add_inst(self, inst):
        self.liste_inst.add(inst)

    def do(self):
        self.liste_inst.do()

    def show(self):
        print(self.nom)
        for inst in self.liste_inst:
            inst.show()
