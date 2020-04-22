from tree.utils.boutons.Bouton import Bouton
from threading import Thread

class Bouton_poussoir(Bouton):
    """
    bouton avec 2 type de scenario, on et off
    """
    def __init__(self, nom, env, preset, liste_scenar):
        Bouton.__init__(self, nom)
        self.liste_scenar = liste_scenar
        self.env = env
        self.preset = preset

    def etat(self):
        return self.env.etat()

    def press(self):
        for scenar in self.liste_scenar:
            print(scenar.nom + "=="+str(scenar.marqueur))
            print(self.env.etat())
            if scenar.marqueur != self.env.etat():
                break
        process = Thread(target=scenar.do)
        process.start()
        self.env.change_scenario_select(scenar)

    def show(self):
        print("bouton poussoir")
        super.show()
        for scenar in self.liste_scenar:
            scenar.show()






