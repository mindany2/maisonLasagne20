from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_etat(Bouton):
    """
    bouton avec une liste de scénario, il en faut obligatoirement un seul de chaque type
    """
    def __init__(self, nom, env, scenar_on, scenar_off):
        Bouton.__init__(self, nom)
        self.env = env
        self.scenar_on = scenar_on
        self.scenar_off = scenar_off

    def press(self, etat = None):
        pile = self.env.get_pile_scenarios()
        scenar = None
        if self.env.etat() != MARQUEUR.ON and etat:
            # on met ON
            pile.push_select()
            scenar = self.scenar_on
        # sinon on met le precedent
        elif not(etat):
            if pile.top() != None:
                scenar = pile.pop()
            else:
                pile.pop()
                scenar = self.scenar_off
        if scenar:
            pile.change_select(scenar)
            scenar.do()


