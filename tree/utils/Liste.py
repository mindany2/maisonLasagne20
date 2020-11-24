from tree.utils.Dico import Dico

class Liste(Dico):
    """
    Permet simplement de stocker un élément
    directement avec son nom
    """
    def __init__(self):
        Dico.__init__(self)

    def add(self, element):
        Dico.add(self, element.nom, element)

