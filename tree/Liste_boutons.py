from tree.Bouton import Bouton


class Liste_boutons:
    """
    Contient la liste des boutons d'une page
    """
    def __init__(self):
        self.liste_boutons = {}

    def add(self, bouton):
        self.liste_boutons[bouton.nom] = bouton

    def __iter__(self):
        return self.liste_boutons.values().__iter__()

    def show(self):
        for btn in self.liste_boutons.values():
            btn.show()

