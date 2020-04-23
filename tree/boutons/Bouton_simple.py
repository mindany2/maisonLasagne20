from threading import Thread
from tree.boutons.Bouton import Bouton

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

    def press(self):
        # on fait le scénario
        process = Thread(target=self.scenar.do)
        process.start()
        # on le renvoie pour qu'il change d'état
        return self.scenar

    def show(self):
        print("bouton simple")
        super.show()
        self.scenar.show()
