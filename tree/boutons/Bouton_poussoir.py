from tree.boutons.Bouton import Bouton
from threading import Thread

class Bouton_poussoir(Bouton):
    """
    bouton avec 2 type de scenario, on et off
    """
    def __init__(self, nom, env, scenar_on, scenar_off):
        Bouton.__init__(self, nom)
        self.scenar_off = scenar_off
        self.scenar_on = scenar_on
        self.env = env

    def etat(self):
        return self.env.etat()

    def press(self):
        if self.etat():
            scenar = self.scenar_off
        else:
            scenar = self.scenar_on
        process = Thread(target=scenar.do)
        process.start()
        return scenar

    def show(self):
        print("bouton poussoir")
        super.show()






