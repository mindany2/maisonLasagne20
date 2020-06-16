from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_choix(Bouton):
    """
    bouton avec une liste de scénario, il passe le l'un à l'autre
    """
    def __init__(self, nom, env, liste_scenar):
        Bouton.__init__(self, nom)
        self.env = env
        self.liste_scenar = liste_scenar

    def press(self, etat_env_principal = None):
        pile = self.env.get_preset_select().get_pile()
        select = 0
        for i,scenar in enumerate(self.liste_scenar):
            if pile.selected() == scenar:
                select = i+1
                if select == len(self.liste_scenar):
                    select = 0
                break
        return self.liste_scenar[select].do()




