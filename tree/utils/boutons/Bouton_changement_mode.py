from tree.utils.boutons.Bouton import Bouton
from tree.Tree import Tree
from threading import Thread

class Bouton_changement_mode(Bouton):
    """
    bouton avec 2 type de scenario, on et off
    """
    def __init__(self):
        Bouton.__init__(self, "mode")

    def etat(self):
        return True

    def reload_name(self):
        self.nom = Tree().get_current_mode().nom

    def press(self):
        Tree().liste_modes.next()
        Tree().change_mode_select(Tree().get_current_mode())
        self.reload_name()

    def show(self):
        print("bouton mode")
        super.show()

