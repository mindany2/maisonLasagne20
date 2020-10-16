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

    def press(self, etat = None):
        pile = self.env.get_preset_select().get_pile()

        scenar = None
        if not(etat):
            # on doit eteindre
            if pile.selected() == self.scenar_deco:
                # si le scenario actuel est celui de ce bouton
                # on passe au précédents
                # sauf si l'état est ON
                scenar = pile.pop()
            else:
                # sinon on le supprime
                pile.remove(self.scenar_deco)
        else:
            # On doit allumer
            if (self.env.etat() != MARQUEUR.ON):
                # si on est pas ON
                pile.push_select()
                scenar = self.scenar_deco
            # sinon on le met à la suite
            else:
                pile.push(self.scenar_deco)

        if scenar and scenar != pile.selected():
            pile.change_select(scenar)
            scenar.do()


