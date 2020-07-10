from threading import Thread
from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_simple(Bouton):
    """
    La base d'un bouton
    """

    def __init__(self, nom, scénar):
        Bouton.__init__(self, nom)
        self.scenar = scénar

    def etat(self):
        return self.scenar.etat

    def get_marqueur(self):
        return self.scenar.get_marqueur()

    def press(self, etat_env_principal = None):
        # on fait le scénario
        self.scenar.do()
        # on le renvoie pour qu'il change d'état
        return self.scenar
