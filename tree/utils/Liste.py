from tree.utils.Dico import Dico

class Liste(Dico):
    """
    Ceci est un dictionnaire, mais ayant pour clef le nom de l'élément
    """
    def __init__(self):
        Dico.__init__(self)

    def add(self, element):
        Dico.add(self, element.nom, element)

