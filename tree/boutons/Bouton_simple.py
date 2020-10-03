from threading import Thread
from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_simple(Bouton):
    """
    La base d'un bouton
    """

    def __init__(self, nom, env, scénar):
        Bouton.__init__(self, nom)
        self.env = env
        self.scenar = scénar

    def etat(self):
        return self.scenar.etat()

    def get_marqueur(self):
        return self.scenar.get_marqueur()

    def press(self, etat = None):
        pile = self.env.get_pile_scenarios()
        # on fait le scénario
        pile.change_select(self.scenar)
        self.scenar.do()
