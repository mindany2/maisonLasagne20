from tree.Dico import Dico

class Liste(Dico):
    """
    Contient la liste des boutons d'une page
    """
    def __init__(self):
        Dico.__init__(self)

    def add(self, element):
        Dico.add(self, element.nom, element)

