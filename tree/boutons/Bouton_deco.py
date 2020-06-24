from tree.boutons.Bouton import Bouton
from tree.scenario.Scenario import MARQUEUR

class Bouton_deco(Bouton):
    """
    bouton avec une liste de scénario, il en faut obligatoirement un seul de chaque type
    """
    def __init__(self, nom, env, scenar_deco):
        Bouton.__init__(self, nom)
        self.env = env
        self.scenar_deco = scenar_deco

    def press(self, etat_env_principal = None):
        pile = self.env.get_preset_select().get_pile()
        if etat_env_principal == MARQUEUR.ON:
            # on doit eteindre
            if pile.selected() == self.scenar_deco:
                # si le scenario actuel est celui de ce bouton
                # on passe au précédents
                return pile.pop().do()
            # sinon on le supprime
            pile.remove(self.scenar_deco)
            return pile.selected()
        # On doit allumer
        pile.push_select()
        return self.scenar_deco.do()

