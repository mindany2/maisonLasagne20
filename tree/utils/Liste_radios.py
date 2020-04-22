from tree.utils.Liste import Liste

class Liste_radios(Liste):
    """
    une liste de boutons lié entre eux comme des radios
    """
    def __init__(self):
        Liste.__init__(self)
        self.element_select = None

    def add(self, element, change = True):
        Liste.add(self, element)
        if self.element_select == None:
            self.element_select = element
            if change:
                # on met le bouton selectionner à On
                self.element_select.change()

    def selected(self):
        return self.element_select

    def change_select(self, element):
        self.element_select.change()
        self.element_select = element
        element.change()

    def next(self):
        self.change_select(Liste.next(self, self.element_select))

        
