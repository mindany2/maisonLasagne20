from tree.scenario.Liste_instructions import Liste_instructions
from threading import Thread


class Scenario:
    """
    La base d'un bouton, juste un état
    """

    def __init__(self, nom, marqueur):
        self.nom = nom
        self.liste_inst = Liste_instructions()
        # le marqueur permet de savoir si le scénario éteint
        # l'environnement ou pas
        self.marqueur = marqueur # si le scénario allume ou éteint les lampes
        self.etat = False

    def add_inst(self, inst):
        self.liste_inst.add(inst)

    def get_marqueur(self):
        return self.marqueur

    def change(self):
        print( "le scenario"+  self.nom +" etat"+ str(self.etat))
        self.etat = not(self.etat)
        print( "le scenario"+  self.nom +" etat"+ str(self.etat))

    def do(self):
        self.liste_inst.do()

    def show(self):
        print(self.nom)
        for inst in self.liste_inst:
            inst.show()
