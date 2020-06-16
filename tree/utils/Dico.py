class Dico:
    """
    C'est un dictionnaire avec quelques fonctions utiles
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

    def next(self, element):
        find = False
        for el in self.liste.values():
            if find:
                return el
            if el == element:
                find = True
        assert(find)
        return list(self.liste.values())[0]



    def get_key(self, element):
        for i,clef in enumerate(self.liste.keys()):
            if self.liste[clef] == element:
                return clef
        return None


    def __iter__(self):
        return self.liste.values().__iter__()

    def keys(self):
        return self.liste.keys().__iter__()

    def est_vide(self):
        return self.liste.keys() == []

    def show(self):
        for element in self.liste.values():
            element.show()

