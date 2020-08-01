from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_poussoir(Bouton):
    """
    bouton avec une liste de scénario, il en faut obligatoirement un seul de chaque type
    """
    def __init__(self, nom, env, scenar):
        Bouton.__init__(self, nom)
        self.env = env
        self.scenar = scenar

    def press(self, etat_env_principal = None, etat = None):
        pile = self.env.get_pile_scenarios()
        if self.scenar.marqueur == MARQUEUR.OFF:
            pile.clear()
        else:
            pile.push_select()
        return self.scenar.do()
