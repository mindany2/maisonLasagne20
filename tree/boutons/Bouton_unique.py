from threading import Thread
from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

from utils.Logger import Logger

class Bouton_unique(Bouton):
    """
    Il ne renvoie pas de scenario,
    Il permet de ne pas interrerer avec d'autres sceanrio
    pour faire les boutons html global
    """

    def __init__(self, nom, scenar_on, scenar_off):
        Bouton.__init__(self, nom)
        self.scenar_on = scenar_on
        self.scenar_off = scenar_off

    def etat(self):
        return self.scenar_on.etat

    def get_marqueur(self):
        return self.scenar_on.get_marqueur()

    def press(self, etat = None):
        Logger.debug("on press bt unique etat = "+str(etat))

        # on fait le scénario s'il n'est pas on
        if etat == None:
            etat = not(self.etat())

        if etat:
            self.scenar_on.do()
            self.scenar_on.etat = True
            self.scenar_off.etat = False
        else:
            self.scenar_off.do()
            self.scenar_on.etat = False
            self.scenar_off.etat = True

        return None
