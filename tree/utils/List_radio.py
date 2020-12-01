from tree.utils.List import List

class List_radio(List):
    """
    Manage the list to have only one selected item at the time
    """
    def __init__(self):
        List.__init__(self)
        self.element_select = None

    def add(self, element, change = True):
        List.add(self, element)
        if self.element_select == None:
            self.element_select = element
            if change:
                self.element_select.etat(True)

    def selected(self):
        return self.element_select

    def change_select(self, element):
        self.element_select.change_etat(False)
        self.element_select = element
        self.element_select.change_etat(True)

    def next(self):
        self.change_select(super().next(self.element_select))

        
