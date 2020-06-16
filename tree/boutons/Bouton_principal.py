from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_principal(Bouton):
    """
    bouton avec une liste de scénario, il en faut obligatoirement un seul de chaque type
    """
    def __init__(self, nom, env, scenar_on, scenar_off):
        Bouton.__init__(self, nom)
        self.env = env
        self.scenar_on = scenar_on
        self.scenar_off = scenar_off

    def press(self, etat_env_principal = None):
        pile = self.env.get_pile_scenarios()
        if self.env.etat() != MARQUEUR.ON:
            pile.push_select()
            return self.scenar_on.do()
        # sinon on met le precedent
        if pile.top() != None:
            if pile.top().marqueur == MARQUEUR.DECO:
                return pile.pop().do()
        pile.pop()
        return self.scenar_off.do()



