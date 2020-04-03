class Dico:
    """
    Contient la liste des boutons d'une page
    """
    def __init__(self):
        self.liste = {}

    def add(self, clef, element):
        self.liste[clef] = element

    def get(self, clef):
        try :
            return self.liste[clef]
        except:
            return None

    def get_index(self, clef):
        for i,key in enumerate(self.liste.keys()):
            if clef == key:
                return i
        return None

    def __iter__(self):
        return self.liste.values().__iter__()

    def keys(self):
        return self.liste.keys().__iter__()

    def show(self):
        for element in self.liste.values():
            element.show()

