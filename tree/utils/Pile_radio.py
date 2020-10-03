from tree.utils.Liste_radios import Liste_radios

class Pile_radio(Liste_radios):
    """
    Stocke les elements précédents
    """
    def __init__(self):
        Liste_radios.__init__(self)
        self.pile = []

    def clear(self):
        self.pile = []
        print([el.nom for el in self.pile])

    def is_present(self, element):
        return self.pile.count(element) == 1

    def push_select(self):
        self.push(self.selected())

    def push(self, element, index=0):
        if index == 0:
            self.pile.append(element)
        else:
            self.pile.insert(index, element)
        print([el.nom for el in self.pile])

    def remove(self, element):
        try:
            self.pile.remove(element)
        except:
            pass
        print([el.nom for el in self.pile])

    def pop(self):
        element = self.top()
        if element != None:
            self.remove(element)
        return element

    def top(self):
        if self.pile:
            return self.pile[-1]
        return None
