from tree.utils.Dico import Dico

class List(Dico):
    """
    Allows to store automically the name to optimise search
    """
    def __init__(self):
        Dico.__init__(self)

    def add(self, element):
        super().add(element.nom, element)

    def remove(self, element):
        super().remove(element.nom)
