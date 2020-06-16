from tree.boutons.Bouton import Bouton
from tree.Tree import Tree

class Bouton_changement_mode(Bouton):
    """
    bouton avec 2 type de scenario, on et off
    """
    def __init__(self, nom):
        Bouton.__init__(self, nom)

    def press(self):
        Tree().liste_modes.next() # on va au mode suivant

    def show(self):
        print("bouton mode")
        super.show()

