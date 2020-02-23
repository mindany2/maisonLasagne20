from tree.Liste_boutons import Liste_boutons

class Liste_boutons_radios(Liste_boutons):
    """
    une liste de boutons lié entre eux comme des radios
    """
    def __init__(self):
        Liste_boutons.__init__(self)
        self.bouton_select = None

    def add(self, bouton):
        Liste_boutons.add(self, bouton)
        if self.bouton_select == None:
            self.bouton_select = bouton
            self.bouton_select.change()

    def change_select(self, bouton):
        self.bouton_select.change()
        self.bouton_select = bouton
        self.bouton_select.change()
        
