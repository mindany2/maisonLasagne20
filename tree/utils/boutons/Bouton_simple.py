from threading import Thread
from tree.utils.boutons.Bouton import Bouton

class Bouton_simple(Bouton):
    """
    La base d'un bouton
    """

    def __init__(self, nom, env, preset, scénar):
        Bouton.__init__(self, nom)
        self.scenar = scénar
        self.env = env
        self.preset = preset

    def etat(self):
        return self.scenar.etat

    def press(self):
        # on fait le scénario
        process = Thread(target=self.scenar.do)
        process.start()
        # on le met comme actif 
        self.env.change_scenario_select(self.scenar)

    def show(self):
        print("bouton simple")
        super.show()
        self.scenar.show()
