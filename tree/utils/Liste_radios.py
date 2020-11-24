from tree.utils.Liste import Liste

class Liste_radios(Liste):
    """
    Permet de gérer les listes radios
    un seul élément selectionner à la fois
    """
    def __init__(self):
        Liste.__init__(self)
        self.element_select = None

    def add(self, element, change = True):
        Liste.add(self, element)
        if self.element_select == None:
            self.element_select = element
            if change:
                # on indique a l'element qu'il est allumer
                self.element_select.etat(True)

    def selected(self):
        return self.element_select

    def change_select(self, element):
        self.element_select.etat(False)
        self.element_select = element
        self.element_select.etat(True)

    def next(self):
        self.change_select(super().next(self.element_select))

        
